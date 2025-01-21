// main.c

#include <stdio.h>
#include <inttypes.h>
#include "sdkconfig.h"
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

// BLE
#include "gap.h"
#include "gatt_svr.h"
#include "nvs_flash.h"
#include "esp_bt.h"

#include "controller.h"
#include "led.h"

// battery
#include "battery.h"

// interrupt on gpio
#include "gpio_interrupt.h"

// i2c config for the color sensor
#include "i2c_config.h"

#include "opt4060.h"
#include "color_predictor.h"

#define LEDC_TIMER LEDC_TIMER_0
#define LEDC_MODE LEDC_LOW_SPEED_MODE
#define LEDC_DUTY_RES LEDC_TIMER_10_BIT // Set duty resolution to 13 bits
#define LEDC_FREQUENCY (15000)          // Frequency in Hertz. Set frequency at 15 kHz

#define MOTOR_A_FWD_GPIO 13
#define MOTOR_A_BWD_GPIO 14
#define MOTOR_B_FWD_GPIO 4
#define MOTOR_B_BWD_GPIO 5

// Global variables
static bool motor_direction[NUM_MOTORS] = {true, true}; // true for forward, false for backward

QueueHandle_t gpio_intr_evt_queue = NULL;
NeuralNetwork nn;

void gpio_interrupt_task(void *pvParameters)
{
    uint32_t io_num;
    for (;;)
    {
        if (xQueueReceive(gpio_intr_evt_queue, &io_num, portMAX_DELAY))
        {
            printf("GPIO[%lu] interrupt occurred (falling edge)!\n", io_num);

            uint16_t red, green, blue, clear;
            opt4060_read_color(&red, &green, &blue, &clear);
            ESP_LOGD("main", "Color values - Red: %d, Green: %d, Blue: %d, Clear: %d, Color: White", red, green, blue, clear);

            if (gpio_get_level(INTERRUPT_PIN) == 0)
            {
                uint32_t color = predict_color(&nn, red, green, blue, clear);
                command_set_game_status(color);
            }
        }
    }
}

void app_main(void)
{
    // Initialize LEDs
    led_init();
    // Initializa Motor
    motor_block_init();
    // BLE Setup -------------------
    nimble_port_init();
    ble_hs_cfg.sync_cb = sync_cb;
    ble_hs_cfg.reset_cb = reset_cb;
    gatt_svr_init();
    ble_svc_gap_device_name_set(device_name);
    nimble_port_freertos_init(host_task);

    // Initialize the motor controller
    controller_init();

    esp_err_t ret = battery_init();
    if (ret != ESP_OK)
    {
        ESP_LOGE("main", "Battery initialization failed");
        return;
    }

    initialize_neural_network(&nn);

    // initilize interrupt for HAL
    configure_gpio_interrupt();
    gpio_intr_evt_queue = gpio_interrupt_get_evt_queue();
    xTaskCreate(gpio_interrupt_task, "gpio_interrupt_task", 2048, NULL, 10, NULL);

    // color sensor
    opt4060_init();

    while (1)
    {

        //        // uncomment this for training data collection
        //        uint16_t red, green, blue, clear;
        //        opt4060_read_color(&red, &green, &blue, &clear);
        //        // NOTE "Color: White" is hardcoded -- rename this to the color you are training for
        //        ESP_LOGI("main", "Color values - Red: %d, Green: %d, Blue: %d, Clear: %d, Color: Black", red, green, blue, clear);

        vTaskDelay(100 / portTICK_PERIOD_MS); // Delay
    }
}
