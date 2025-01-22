#include "controller.h"
#include "motor.h"
#include <stdio.h>
#include "esp_log.h"

static MotorCommand g_current_command;
static SemaphoreHandle_t g_command_mutex;
static TaskHandle_t g_controller_task_handle = NULL;
static TimerHandle_t g_command_timer;
static TimerHandle_t g_command_game_timer;

// game state
game_status g_state;

// we need to make sure to give immunity for 10 seconds after we have a hit an obstacle
static TickType_t cooldown_end = 0;

void command_set_game_status(uint32_t status)
{

    if (g_state == GAME_OFF)
    {
        // set the game state
        g_state = status;
        uint32_t period = 0;

        TickType_t current_time = xTaskGetTickCount();

        // set the timer period
        switch (status)
        {
        case GAME_GREEN:
            if (current_time < cooldown_end)
            {
                ESP_LOGW("controller", "Cooldown. Ignoring.");
                period = 0;
                // turn off the game effect
                g_state = GAME_OFF;
            }
            else
            {
                ESP_LOGW("controller", "Set GREEN");
                led_set_flash_mode(LED_FLASH_ALL);
                period = 1000;                                     // 1 second
                cooldown_end = current_time + pdMS_TO_TICKS(5000); // 5 second cool down
            }
            break;
        case GAME_RED:
            period = 1000; // 1 second
            ESP_LOGW("controller", "Set RED");
            break;
        case GAME_WHITE:
            period = 10000; // 10 seconds
            ESP_LOGW("controller", "Set WHITE");
            led_set_flash_mode(LED_FLASH_FRONT_ALTERNATE);
            break;
        case GAME_BLACK:
            period = 10000; // 10 seconds
            ESP_LOGW("controller", "Set BLACK");
            led_set_flash_mode(LED_FLASH_BACK);
            break;
        case GAME_YELLOW:
            period = 1000; // 1 second
            ESP_LOGW("controller", "Set YELLOW");
            break;
        default:
            period = 0;
            break;
        }

        // start the timer
        if (xTimerIsTimerActive(g_command_game_timer) == pdFALSE && period != 0)
        {
            ESP_LOGW("controller", "Starting game timer");
            xTimerChangePeriod(g_command_game_timer, pdMS_TO_TICKS(period), 0);
            xTimerStart(g_command_game_timer, 0);
        }
    }
}

// stop motor A&B
void command_timer_callback(TimerHandle_t xTimer)
{
    ESP_LOGI("controller", "Timer expired, stopping motors");

    // Set motor speeds to 0 when the timer expires
    MotorUpdate update_a = {0, 0, 0};
    MotorUpdate update_b = {1, 0, 0};

    BaseType_t xStatus;
    xStatus = xQueueSend(motor_queue[0], &update_a, 0);
    if (xStatus != pdPASS)
    {
        ESP_LOGE("controller", "Failed to send stop update for Motor A");
    }
    xStatus = xQueueSend(motor_queue[1], &update_b, 0);
    if (xStatus != pdPASS)
    {
        ESP_LOGE("controller", "Failed to send stop update for Motor B");
    }
}

void command_game_timer_callback(TimerHandle_t xTimer)
{
    ESP_LOGW("controller", "Game timer expired");
    g_state = GAME_OFF;
    led_set_flash_mode(LED_CONST);
}

#define SPEEDUP 10
#define SLOWDOWN 10
#define SPINOUT_SPEED 60

void set_motor_command(MotorCommand command)
{
    // modify the command based on the game state
    switch (g_state)
    {
    case GAME_GREEN: // spin out for now
        // trying to detect if we are moving forward or not
        command.MotorASpeed = SPINOUT_SPEED;
        command.MotorADirection = 1;
        command.MotorBSpeed = SPINOUT_SPEED;
        command.MotorBDirection = 0;
        command.seconds = 10;
        break;
    case GAME_RED: // speed up
        // trying to detect if we are moving forward or not
        if (command.MotorASpeed < SPEEDUP && command.MotorBSpeed > SPEEDUP)
        {
            command.MotorASpeed += SPEEDUP;
            command.MotorBSpeed += SPEEDUP;
        }
        break;
    case GAME_WHITE: // speed up
        // trying to detect if we are moving forward or not
        if (command.MotorASpeed > SPEEDUP && command.MotorBSpeed > SPEEDUP)
        {
            ESP_LOGW("controller", "speeding up!");
            command.MotorASpeed += SPEEDUP;
            command.MotorBSpeed += SPEEDUP;
        }

        break;
    case GAME_BLACK: // slow down
        if (command.MotorASpeed > SLOWDOWN && command.MotorBSpeed > SLOWDOWN)
        {
            command.MotorASpeed -= SLOWDOWN;
            command.MotorBSpeed -= SLOWDOWN;
        }
        break;
    case GAME_YELLOW: // spin out
        break;
    default:
        break;
    }

    if (xTimerIsTimerActive(g_command_timer) == pdFALSE)
    {
        ESP_LOGI("controller", "Starting timer");
        xTimerChangePeriod(g_command_timer, pdMS_TO_TICKS(command.seconds * 100), 0);
        xTimerStart(g_command_timer, 0);
    }
    else
    {
        ESP_LOGI("controller", "Resetting timer");
        xTimerReset(g_command_timer, 0);
        xTimerStart(g_command_timer, 0);
    }

    g_current_command = command;

    if (g_controller_task_handle != NULL)
    {
        // Notify the controller task to process the new command
        xTaskNotifyGive(g_controller_task_handle);
    }

    ESP_LOGI("controller", " set_motor_command: Timer set for %lu S", command.seconds);
}

void controller_task(void *pvParameters)
{
    while (1)
    {
        // Wait for a notification to process the command
        ulTaskNotifyTake(pdTRUE, portMAX_DELAY);

        MotorCommand command = g_current_command;

        // Send motor updates to the queue
        MotorUpdate update_a = {0, command.MotorASpeed, command.MotorADirection};
        MotorUpdate update_b = {1, command.MotorBSpeed, command.MotorBDirection};

        BaseType_t xStatus;
        xStatus = xQueueSend(motor_queue[0], &update_a, 0);
        if (xStatus != pdPASS)
        {
            ESP_LOGE("controller", "Failed to send update for Motor A");
        }
        xStatus = xQueueSend(motor_queue[1], &update_b, 0);
        if (xStatus != pdPASS)
        {
            ESP_LOGE("controller", "Failed to send update for Motor B");
        }

        ESP_LOGI("controller", "Motor 0 set to speed %d%%, direction %s", command.MotorASpeed,
                 command.MotorADirection == 0 ? "FORWARD" : "BACKWARD");
        ESP_LOGI("controller", "Motor 1 set to speed %d%% , direction %s", command.MotorBSpeed,
                 command.MotorBDirection == 0 ? "FORWARD" : "BACKWARD");

        ESP_LOGI("controller", "set motor speeds via controller");
    }
}

void controller_init()
{
    g_command_mutex = xSemaphoreCreateMutex();
    if (g_command_mutex == NULL)
    {
        ESP_LOGE("controller", "Failed to create command mutex");
        return;
    }

    g_command_timer = xTimerCreate("CommandTimer", pdMS_TO_TICKS(1000), pdFALSE, (void *)0, command_timer_callback);
    if (g_command_timer == NULL)
    {
        ESP_LOGE("controller", "Failed to create command timer");
        return;
    }

    g_command_game_timer = xTimerCreate("CommandGameTimer", pdMS_TO_TICKS(1000),
                                      pdFALSE, (void *)0, command_game_timer_callback);

    if (g_command_game_timer == NULL)
    {
        ESP_LOGE("controller", "Failed to create command timer");
        return;
    }

    xTaskCreate(controller_task, "controller_task", 2048, NULL, 5, &g_controller_task_handle);

    // set the game state to GAME_OFF
    g_state = GAME_OFF;
}
