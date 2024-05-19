# AUTHOR:   SANDER BETZ
# ST-NR:    6070000
# ST-MAIL:  S.H.R.Betz@student.tudelft.nl

# Put imports here
import marsatm
import math
import matplotlib.pyplot as plt

# Main code
g_0 = 3.711
R = 191.84

# Vehicle properties
start_velocity = 262
start_mass = 5500
start_angle = math.radians(-20)             # radians


mass = 5500
C_d_mult_S = 4.92
v_exit = 4400
dry_mass = 699.0
fuel_mass = mass - dry_mass
k_v = 0.05
v_y_ref = -2.0

h_t = 10000
delta_time = 0.1    # Seconds

def main():
    mars_atmosphere_properties = marsatm.marsinit()

    time_log = []
    y_log = []
    x_log = []
    vy_log = []
    vx_log = []
    mdot_log = []
    gamma_log = []
    velocity_log = []

    landed = False

    height = 20000                  # meters
    x = 0
    angle = math.radians(-20)

    total_time = 0

    v_x = start_velocity * math.cos(start_angle)
    v_y = start_velocity * math.sin(start_angle)
    v_total = math.sqrt(v_x**2 + v_y**2)

    mass = 5500

    while not landed:
        pressure, temperature, density, sound_vel = marsatm.marsatm(height, mars_atmosphere_properties)

        F_gravity = mass * g_0
        delta_v_y = v_y_ref - v_y
        if height > h_t:
            m_dot = 0
        else:
            m_dot = (mass * g_0) / v_exit + k_v * delta_v_y

        if m_dot > 5.:
            m_dot = 5.
        F_thrust = m_dot * v_exit
        F_drag = (1/2) * density * v_total ** 2 * C_d_mult_S

        accel_x = (-F_thrust * math.cos(angle) - F_drag * math.cos(angle)) / mass
        accel_y = (F_thrust * math.sin(angle) + F_drag * math.sin(angle) - mass * g_0) / mass

        # Update all values
        v_x += accel_x * delta_time
        v_y += accel_y * delta_time
        v_total = math.sqrt(v_x ** 2 + v_y ** 2)
        height += v_y * delta_time
        x += v_x * delta_time
        angle = math.atan(v_y / v_x)
        mass -= m_dot * delta_time

        time_log.append(total_time)
        x_log.append(x)
        y_log.append(height)
        vx_log.append(v_x)
        vy_log.append(v_y)
        velocity_log.append(v_total)
        gamma_log.append(math.degrees(angle))
        mdot_log.append(m_dot)

        print(f'Time: {round(total_time, 2)}, Alt: {round(height, 2)}, Vel: {round(v_total, 2)}, '
              f'Vel x: {round(v_x, 2)}, Vel y: {round(v_y, 2)}, Angle: {round(angle, 2)} '
              f'Thrust: {F_thrust}, Accel x: {accel_x}, Accel y: {accel_y} '
              f'Mass: {mass}, F_drag: {F_drag}')

        total_time += delta_time
        if height < 100:
            break

    # Generate the plots
    # Make 2 rows of 3 graphs, start with plot 1
    plt.figure(figsize=(18, 8))

    plt.subplot(231)
    plt.plot(x_log, y_log)
    plt.title('Trajectory')
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')

    plt.subplot(232)
    plt.plot(vx_log, vy_log)
    plt.title('Speed')
    plt.xlabel('x velocity')
    plt.ylabel('y velocity')

    plt.subplot(233)
    plt.plot(time_log, mdot_log)
    plt.title('Mdot vs time')
    plt.xlabel('Time [s]')
    plt.ylabel('m_dot [kg/s]')

    # Second row: plot 4-6
    plt.subplot(234)
    plt.plot(time_log, y_log)
    plt.title('Alt vs time')
    plt.xlabel('Time [s]')
    plt.ylabel('Height [m]')

    plt.subplot(235)
    plt.plot(time_log, velocity_log)
    plt.plot(time_log, vx_log, color='r')
    plt.plot(time_log, vy_log, color='g')
    plt.title('Spd vs time')
    plt.xlabel('Time [s]')
    plt.ylabel('Velocity [m/s]')

    plt.subplot(236)
    plt.plot(time_log, gamma_log)
    plt.title('Gamma vs time')
    plt.xlabel('Time [s]')
    plt.ylabel('Angle [deg]')

    # Show plot window
    plt.show()

    print('Simulation finished after: ', total_time, 'seconds.')

if __name__ == '__main__':
    main()
