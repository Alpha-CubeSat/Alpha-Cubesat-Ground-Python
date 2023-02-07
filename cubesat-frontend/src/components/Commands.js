export const mission_mode_init = {
	name: "mission_mode_init",
    title: "Mode: Initialization",
    description: "Sends command [mission::mode_initialization]"
}

export const mission_mode_low_power = {
	name: "mission_mode_low_power",
    title: "Mode: Low Power",
    description: "Sends command [mission::mode_low_power]"
}

export const mission_mode_deployment = {
	name: "mission_mode_deployment",
    title: "Mode: Deployment",
    description: "Sends command [mission::mode_deployment]"
}

export const mission_mode_safe = {
	name: "mission_mode_safe",
    title: "Mode: Safe",
    description: "Sends command [mission::mode_safe]"
}

export const mission_mode_standby = {
	name: "mission_mode_standby",
    title: "Mode: Standby",
    description: "Sends command [mission::mode_standby]"
}

export const burnwire_arm_true = {
	name: "burnwire_arm_true",
    title: "Arm: True",
    description: "Sends command [burnwire::arm_true]"
}

export const burnwire_arm_false = {
	name: "burnwire_arm_false",
    title: "Arm: False",
    description: "Sends command [burnwire::arm_false]"
}

export const burnwire_fire_true = {
	name: "burnwire_fire_true",
    title: "Fire: True",
    description: "Sends command [burnwire::fire_true]"
}

export const burnwire_fire_false = {
	name: "burnwire_fire_false",
    title: "Fire: False",
    description: "Sends command [burnwire::fire_false]"
}

export const burnwire_burn_time = {
	name: "burnwire_burn_time",
    title: "Burn Time",
    description: "Sends command [burnwire::burn_time] with the specified seconds",
    fields: [
        {
            title: "Burn Time"
        }
    ]
}

export const burnwire_arm_time = {
	name: "burnwire_arm_time",
    title: "Arm Time",
    description: "Sends command [burnwire::arm_time] with the specified seconds",
    fields: [
        {
            title: "Arm Time"
        }
    ]
}

export const rockblock_downlink_period = {
	name: "rockblock_downlink_period",
    title: "Downlink Period",
    description: "Sends command [rockblock::downlink_period] with the specified seconds",
    fields: [
        {
            title: "Downlink Period"
        }
    ]
}

export const request_img_fragment = {
	name: "request_img_fragment",
    title: "Request Image Fragment",
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

export const take_photo_true = {
	name: "take_photo_true",
    title: "Take Photo: True",
    description: "Sends command [camera::take_photo_true]"
}

export const take_photo_false = {
	name: "take_photo_false",
    title: "Take Photo: False",
    description: "Sends command [camera::take_photo_false]"
}

export const temperature_mode_active = {
	name: "temperature_mode_active",
    title: "Mode: Active",
    description: "Sends command [temperature::mode_active]"
}

export const temperature_mode_inactive = {
	name: "temperature_mode_inactive",
    title: "Mode: Inactive",
    description: "Sends command [temperature::mode_inactive]"
}

export const acs_mode_full = {
	name: "acs_mode_full",
    title: "Mode: Full",
    description: "Sends command [acs::mode_full]"
}

export const acs_mode_simple = {
	name: "acs_mode_simple",
    title: "Mode: Simple",
    description: "Sends command [acs::mode_simple]"
}

export const acs_mode_off = {
	name: "acs_mode_off",
    title: "Mode: Off",
    description: "Sends command [acs::mode_off]"
}

export const acs_mag_x = {
	name: "acs_mag_x",
    title: "Mag: X",
    description: "Sends command [acs::mag_x]"
}

export const acs_mag_y = {
	name: "acs_mag_y",
    title: "Mag: Y",
    description: "Sends command [acs::mag_y]"
}

export const acs_mag_z = {
	name: "acs_mag_z",
    title: "Mag: Z",
    description: "Sends command [acs::mag_z]"
}

export const camera_turn_on = {
	name: "camera_turn_on",
    title: "Turn On",
    description: "Sends command [camera::turn_on]"
}

export const camera_turn_off = {
	name: "camera_turn_off",
    title: "Turn Off",
    description: "Sends command [camera::turn_off]"
}

export const fault_mode_active = {
	name: "fault_mode_active",
    title: "Fault Mode: Active",
    description: "Sends command [fault::mode_active]"
}

export const fault_mode_inactive = {
	name: "fault_mode_inactive",
    title: "Fault Mode: Inactive",
    description: "Sends command [fault::mode_inactive]"
}

export const fault_check_mag_x_true = {
	name: "fault_check_mag_x_true",
    title: "Check Mag X: True",
    description: "Sends command [fault::check_mag_x_true]"
}

export const fault_check_mag_x_false = {
	name: "fault_check_mag_x_false",
    title: "Check Mag X: False",
    description: "Sends command [fault::check_mag_x_false]"
}

export const fault_check_mag_y_true = {
	name: "fault_check_mag_y_true",
    title: "Check Mag Y: True",
    description: "Sends command [fault::check_mag_y_true]"
}

export const fault_check_mag_y_false = {
	name: "fault_check_mag_y_false",
    title: "Check Mag Y: False",
    description: "Sends command [fault::check_mag_y_false]"
}

export const fault_check_mag_z_true = {
	name: "fault_check_mag_z_true",
    title: "Check Mag Z: True",
    description: "Sends command [fault::check_mag_z_true]"
}

export const fault_check_mag_z_false = {
	name: "fault_check_mag_z_false",
    title: "Check Mag Z: False",
    description: "Sends command [fault::check_mag_z_false]"
}

export const fault_check_gyro_x_true = {
	name: "fault_check_gyro_x_true",
    title: "Check Gyro X: True",
    description: "Sends command [fault::check_gyro_x_true]"
}

export const fault_check_gyro_x_false = {
	name: "fault_check_gyro_x_false",
    title: "Check Gyro X: False",
    description: "Sends command [fault::check_gyro_x_false]"
}

export const fault_check_gyro_y_true = {
	name: "fault_check_gyro_y_true",
    title: "Check Gyro Y: True",
    description: "Sends command [fault::check_gyro_y_true]"
}

export const fault_check_gyro_y_false = {
	name: "fault_check_gyro_y_false",
    title: "Check Gyro Y: False",
    description: "Sends command [fault::check_gyro_y_false]"
}

export const fault_check_gyro_z_true = {
	name: "fault_check_gyro_z_true",
    title: "Check Gyro Z: True",
    description: "Sends command [fault::check_gyro_z_true]"
}

export const fault_check_gyro_z_false = {
	name: "fault_check_gyro_z_false",
    title: "Check Gyro Z: False",
    description: "Sends command [fault::check_gyro_z_false]"
}

export const fault_check_temp_c_true = {
	name: "fault_check_temp_c_true",
    title: "Check Temp: True",
    description: "Sends command [fault::check_temp_c_true]"
}

export const fault_check_temp_c_false = {
	name: "fault_check_temp_c_false",
    title: "Check Temp: False",
    description: "Sends command [fault::check_temp_c_false]"
}

export const fault_check_solar_true = {
	name: "fault_check_solar_true",
    title: "Check Solar Curr: True",
    description: "Sends command [fault::check_solar_current_true]"
}

export const fault_check_solar_false = {
	name: "fault_check_solar_false",
    title: "Check Solar Curr: False",
    description: "Sends command [fault::check_solar_current_false]"
}

export const fault_check_voltage_true = {
	name: "fault_check_voltage_true",
    title: "Check Voltage: True",
    description: "Sends command [fault::check_voltage_true]"
}

export const fault_check_voltage_false = {
	name: "fault_check_voltage_false",
    title: "Check Voltage: False",
    description: "Sends command [fault::check_voltage_false]"
}