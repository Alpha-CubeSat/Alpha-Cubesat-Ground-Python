mission_mode_init = {
    name: "Mode: Initialization",
    description: "Sends command [mission::mode_initialization]"
}

mission_mode_low_power = {
    name: "Mode: Low Power",
    description: "Sends command [mission::mode_low_power]"
}

mission_mode_deployment = {
    name: "Mode: Deployment",
    description: "Sends command [mission::mode_deployment]"
}

mission_mode_safe = {
    name: "Mode: Safe",
    description: "Sends command [mission::mode_safe]"
}

mission_mode_standby = {
    name: "Mode: Standby",
    description: "Sends command [mission::mode_standby]"
}

burnwire_arm_true = {
    name: "Arm: True",
    description: "Sends command [burnwire::arm_true]"
}

burnwire_arm_false = {
    name: "Arm: False",
    description: "Sends command [burnwire::arm_false]"
}

burnwire_fire_true = {
    name: "Fire: True",
    description: "Sends command [burnwire::fire_true]"
}

burnwire_fire_false = {
    name: "Fire: False",
    description: "Sends command [burnwire::fire_false]"
}

burnwire_burn_time = {
    name: "Burn Time",
    description: "Sends command [burnwire::burn_time] with the specified seconds",
    fields: [
        {
            title: "Burn Time"
        }
    ]
}

burnwire_arm_time = {
    name: "Arm Time",
    description: "Sends command [burnwire::arm_time] with the specified seconds",
    fields: [
        {
            title: "Arm Time"
        }
    ]
}

rockblock_downlink_period = {
    name: "Downlink Period",
    description: "Sends command [rockblock::downlink_period] with the specified seconds",
    fields: [
        {
            title: "Downlink Period"
        }
    ]
}

request_img_fragment = {
    name: "Request Image Fragment",
    description: "Requests the specified image fragment from the specified camera",
    fields: [
        {
            title: "Camera Serial Number"
        },
        {
            title: "Image Fragment Number"
        }
    ]
}

take_photo_true = {
    name: "Take Photo: True",
    description: "Sends command [camera::take_photo_true]"
}

take_photo_false = {
    name: "Take Photo: False",
    description: "Sends command [camera::take_photo_false]"
}

temperature_mode_active = {
    name: "Mode: Active",
    description: "Sends command [temperature::mode_active]"
}

temperature_mode_inactive = {
    name: "Mode: Inactive",
    description: "Sends command [temperature::mode_inactive]"
}

acs_mode_full = {
    name: "Mode: Full",
    description: "Sends command [acs::mode_full]"
}

acs_mode_simple = {
    name: "Mode: Simple",
    description: "Sends command [acs::mode_simple]"
}

acs_mode_off = {
    name: "Mode: Off",
    description: "Sends command [acs::mode_off]"
}

acs_mag_x = {
    name: "Mag: X",
    description: "Sends command [acs::mag_x]"
}

acs_mag_y = {
    name: "Mag: Y",
    description: "Sends command [acs::mag_y]"
}

acs_mag_z = {
    name: "Mag: Z",
    description: "Sends command [acs::mag_z]"
}

camera_turn_on = {
    name: "Turn On",
    description: "Sends command [camera::turn_on]"
}

camera_turn_off = {
    name: "Turn Off",
    description: "Sends command [camera::turn_off]"
}

fault_mode_active = {
    name: "Fault Mode: Active",
    description: "Sends command [fault::mode_active]"
}

fault_mode_inactive = {
    name: "Fault Mode: Inactive",
    description: "Sends command [fault::mode_inactive]"
}

fault_check_mag_x_true = {
    name: "Check Mag X: True",
    description: "Sends command [fault::check_mag_x_true]"
}

fault_check_mag_x_false = {
    name: "Check Mag X: False",
    description: "Sends command [fault::check_mag_x_false]"
}

fault_check_mag_y_true = {
    name: "Check Mag Y: True",
    description: "Sends command [fault::check_mag_y_true]"
}

fault_check_mag_y_false = {
    name: "Check Mag Y: False",
    description: "Sends command [fault::check_mag_y_false]"
}

fault_check_mag_z_true = {
    name: "Check Mag Z: True",
    description: "Sends command [fault::check_mag_z_true]"
}

fault_check_mag_z_false = {
    name: "Check Mag Z: False",
    description: "Sends command [fault::check_mag_z_false]"
}

fault_check_gyro_x_true = {
    name: "Check Gyro X: True",
    description: "Sends command [fault::check_gyro_x_true]"
}

fault_check_gyro_x_false = {
    name: "Check Gyro X: False",
    description: "Sends command [fault::check_gyro_x_false]"
}

fault_check_gyro_y_true = {
    name: "Check Gyro Y: True",
    description: "Sends command [fault::check_gyro_y_true]"
}

fault_check_gyro_y_false = {
    name: "Check Gyro Y: False",
    description: "Sends command [fault::check_gyro_y_false]"
}

fault_check_gyro_z_true = {
    name: "Check Gyro Z: True",
    description: "Sends command [fault::check_gyro_z_true]"
}

fault_check_gyro_z_false = {
    name: "Check Gyro Z: False",
    description: "Sends command [fault::check_gyro_z_false]"
}

fault_check_temp_c_true = {
    name: "Check Temp: True",
    description: "Sends command [fault::check_temp_c_true]"
}

fault_check_temp_c_false = {
    name: "Check Temp: False",
    description: "Sends command [fault::check_temp_c_false]"
}

fault_check_solar_true = {
    name: "Check Solar Curr: True",
    description: "Sends command [fault::check_solar_current_true]"
}

fault_check_solar_false = {
    name: "Check Solar Curr: False",
    description: "Sends command [fault::check_solar_current_false]"
}

fault_check_voltage_true = {
    name: "Check Voltage: True",
    description: "Sends command [fault::check_voltage_true]"
}

fault_check_voltage_false = {
    name: "Check Voltage: False",
    description: "Sends command [fault::check_voltage_false]"
}