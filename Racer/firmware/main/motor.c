#include "motor.h"
#include <stdio.h>
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "freertos/semphr.h"
#include "esp_chip_info.h"
#include "esp_flash.h"
#include "esp_system.h"
#include "esp_log.h"
#include "driver/ledc.h"
#include "driver/gpio.h"
#include "motor.h"

QueueHandle_t motor_queue[2];
SemaphoreHandle_t motor_start_semaphore;

static int config_ledc_timer();
void configure_motor_pwm(int gpio, ledc_channel_t channel)
{
    ledc_channel_config_t ledc_channel = {
        .speed_mode = LEDC_LOW_SPEED_MODE,
        .channel = channel,
        .timer_sel = LEDC_TIMER_0,
        .intr_type = LEDC_INTR_DISABLE,
        .gpio_num = gpio,
        .duty = 0,
        .hpoint = 0};
    esp_err_t err = ledc_channel_config(&ledc_channel);
    if (err != ESP_OK)
    {
        ESP_LOGE("motor", "LEDC Channel Config failed for GPIO %d: %s", gpio, esp_err_to_name(err));
    }
}

void set_motor_speed(int motor_index, int speed_percent, bool direction)
{
    if (motor_index < 0 || motor_index >= NUM_MOTORS)
    {
        ESP_LOGE("motor", "Invalid motor index");
        return;
    }

    // Ensure speed_percent is between MIN_SPEED_PERCENT and 100
    speed_percent = (speed_percent < MIN_SPEED_PERCENT) ? 0 : (speed_percent > 100) ? 100
                                                                                    : speed_percent;

    // Map MIN_SPEED_PERCENT-100 to MIN_DUTY-MAX_DUTY
    int duty;
    if (speed_percent == 0)
    {
        duty = 0;
    }
    else
    {
        int min_duty = (MIN_SPEED_PERCENT * MAX_DUTY) / 100;
        duty = min_duty + ((speed_percent - MIN_SPEED_PERCENT) * (MAX_DUTY - min_duty)) / (100 - MIN_SPEED_PERCENT);
    }

    ledc_channel_t fwd_channel = (ledc_channel_t)(motor_index * 2);
    ledc_channel_t bwd_channel = (ledc_channel_t)(motor_index * 2 + 1);

    ledc_set_duty(LEDC_LOW_SPEED_MODE, fwd_channel, direction ? duty : 0);
    ledc_set_duty(LEDC_LOW_SPEED_MODE, bwd_channel, direction ? 0 : duty);
    ledc_update_duty(LEDC_LOW_SPEED_MODE, fwd_channel);
    ledc_update_duty(LEDC_LOW_SPEED_MODE, bwd_channel);

    ESP_LOGD("motor", "Motor %d set to speed %d%% (duty %d), direction %s",
             motor_index, speed_percent, duty, direction ? "FORWARD" : "BACKWARD");
}

void soft_start_motor(int motor_index, int target_speed, bool target_direction)
{
    static int current_speed[NUM_MOTORS] = {0};
    static bool current_direction[NUM_MOTORS] = {true, true};

    int start_speed = current_speed[motor_index];
    bool start_direction = current_direction[motor_index];

    // If direction is changing, first slow down to 0
    if (start_direction != target_direction && start_speed > 0)
    {
        ESP_LOGD("motor", "slow stopping motor %i", motor_index);
        for (int speed = start_speed; speed >= MIN_SPEED_PERCENT; speed--)
        {
            set_motor_speed(motor_index, speed, start_direction);
            vTaskDelay(SOFT_START_DELAY_MS / portTICK_PERIOD_MS);
        }
        set_motor_speed(motor_index, 0, start_direction);
        start_speed = 0;
    }

    // Now ramp up to target speed in the correct direction
    if (target_speed > 0)
    {
        ESP_LOGD("motor", "ramping up motor %i", motor_index);
        if (start_speed == 0)
        {
            ESP_LOGD("motor", "initial speed was 0 %i", motor_index);
            set_motor_speed(motor_index, MIN_SPEED_PERCENT, target_direction);
            vTaskDelay(SOFT_START_DELAY_MS * 2 / portTICK_PERIOD_MS); // Longer delay for initial start
            start_speed = MIN_SPEED_PERCENT;
        }

        int step = (target_speed > start_speed) ? 1 : -1;
        for (int speed = start_speed; speed != target_speed; speed += step)
        {
            set_motor_speed(motor_index, speed, target_direction);
            vTaskDelay(SOFT_START_DELAY_MS / portTICK_PERIOD_MS);
        }
    }
    else
    {
        ESP_LOGD("motor", "direct set on motor %i", motor_index);
        set_motor_speed(motor_index, 0, target_direction);
    }

    // Ensure we reach exactly the target speed
    set_motor_speed(motor_index, target_speed, target_direction);

    // Update current speed and direction
    current_speed[motor_index] = target_speed;
    current_direction[motor_index] = target_direction;
    ESP_LOGD("motor", "done with motor %i", motor_index);
}

void motor_task(void *pvParameters)
{
    int motor_index = (int)pvParameters;
    MotorUpdate update;
    while (1)
    {
        if (xQueueReceive(motor_queue[0], &update, pdMS_TO_TICKS(10)) == pdTRUE)
        {
            ESP_LOGI("Motor", "motor index %i speed %i direction %i", update.motor_index, update.speed_percent,
                     update.direction);
            set_motor_speed(update.motor_index, update.speed_percent, update.direction);
        }
        if (xQueueReceive(motor_queue[1], &update, pdMS_TO_TICKS(10)) == pdTRUE)
        {
            ESP_LOGI("Motor", "motor index %i speed %i direction %i", update.motor_index, update.speed_percent,
                     update.direction);
            set_motor_speed(update.motor_index, update.speed_percent, update.direction);
        }
    }
}

int config_ledc_timer()
{
    // 配置 LEDC 定时器
    ledc_timer_config_t ledc_timer = {
        .speed_mode = LEDC_MODE,
        .timer_num = LEDC_TIMER,
        .duty_resolution = LEDC_DUTY_RES,
        .freq_hz = LEDC_FREQUENCY,
        .clk_cfg = LEDC_AUTO_CLK};
    esp_err_t err = ledc_timer_config(&ledc_timer);
    if (err != ESP_OK)
    {
        printf("LEDC Timer Config failed: %s\n", esp_err_to_name(err));
        return 0;
    }
    return 1;
}

int motor_block_init(void)
{
    int ret_ = 0;
    if (config_ledc_timer() == 0)
    {
        return ret_;
    }
    // Configure Motors
    configure_motor_pwm(MOTOR_A_FWD_GPIO, LEDC_CHANNEL_0);
    configure_motor_pwm(MOTOR_A_BWD_GPIO, LEDC_CHANNEL_1);
    configure_motor_pwm(MOTOR_B_FWD_GPIO, LEDC_CHANNEL_2);
    configure_motor_pwm(MOTOR_B_BWD_GPIO, LEDC_CHANNEL_3);

    // Create motor queue
    motor_queue[0] = xQueueCreate(MOTOR_QUEUE_SIZE, sizeof(MotorUpdate));
    if (motor_queue[0] == NULL)
    {
        printf("Failed to create motor queue\n");
        return ret_;
    }
    motor_queue[1] = xQueueCreate(MOTOR_QUEUE_SIZE, sizeof(MotorUpdate));
    if (motor_queue[1] == NULL)
    {
        printf("Failed to create motor queue\n");
        return ret_;
    }

    // Create semaphore for synchronizing motor start
    motor_start_semaphore = xSemaphoreCreateCounting(4, 0);
    if (motor_start_semaphore == NULL)
    {
        printf("Failed to create motor start semaphore\n");
        return ret_;
    }

    // Create motor tasks for Motor A and Motor B
    xTaskCreate(motor_task, "motor_task_A", 2048, (void *)0, 1, NULL);
    xTaskCreate(motor_task, "motor_task_B", 2048, (void *)1, 1, NULL);
    return (ret_ = 1);
}
