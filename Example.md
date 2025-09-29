# Example of Kalman Filter

The scenario is:

- We have a gyroscope and accelerometer attached to a device.
- We want to estimate the true rotation about the X and Y axis of
  the device.
- The gyroscope gives us rotational velocity and the accelerometer
  gives us acceleration in 3 axis.
- We can assume that when the accelerometer is at $\langle 0, 0, g \rangle$,
  the device is at 0 degrees rotation about X and Y.

The state would be:

$$
x = \begin{bmatrix}
\theta \\ \phi \\ b_{\theta} \\ b_{\phi}
\end{bmatrix}
$$

Where $b_{\theta}$ and $b_{\phi}$ are the gyroscope biases, these
are systemic errors in the gyroscope measurements that may shift
over time.

The measurements are:

$$
z = \begin{bmatrix}
  \theta \\ \phi
\end{bmatrix}
$$

> [!NOTE]
> You may notice that the gyroscope measurements are not present
> here.
>
> This is because a "measurement" in the formal sense is a direct
> observation of the system state, since $\omega$ is not part of
> our system state, we cannot put it in the measurements vector.
>
> The reason why $\omega$ is not part of our system state is
> elaborated below.

$$H = I$$

Our full system would look like this:

$$
\begin{aligned}
\theta_{k} &= \theta_{k-1} + \Delta t (\omega_{\theta} - b_{\theta}) \\
\phi_{k} &= \phi_{k-1} + \Delta t (\omega_{\phi} - b_{\phi}) \\
b_{\theta, k} &= b_{\theta,k-1} \\
b_{\phi, k} &= b_{\phi,k-1} \\
\end{aligned}
$$

We subtract $b$ from $\omega$ because $b$ is incorporated in the
measurement of $\omega$, therefore we would want to use our best
estimate for the systemic gyroscope bias to remove that bias from
our measurements.

Here, in an ideal setting, the biases $b$ would not change over
time, however, it is possible that due to temperature changes and
other environment factors that $b$ will change over time.

Thus, the state transition model would be.

$$
F = \begin{bmatrix}
  1 & 0 & -\Delta t & 0 \\
  0 & 1 & 0 & -\Delta t \\
  0 & 0 & 1 & 0 \\
  0 & 0 & 0 & 1 \\
\end{bmatrix}
$$

$$
B = \begin{bmatrix}
  \Delta t & 0 \\
  0 & \Delta t \\
  0 & 0 \\
  0 & 0
\end{bmatrix}
$$

$$
u = \begin{bmatrix}
  \omega_{\theta} \\
  \omega_{\phi}
\end{bmatrix}
$$

Process noise is some random variance in gyro measurements and
gyro bias.

$$
Q = \begin{bmatrix}
  \sigma_{\omega_{\theta}}^2 \Delta t^{2} & 0 & 0 & 0 \\
  0 & \sigma_{\omega_{\phi}}^2 \Delta t^{2} & 0 & 0 \\
  0 & 0 & \sigma_{b_{\theta}}^2 & 0 \\
  0 & 0 & 0 & \sigma_{b_{\phi}}^2
\end{bmatrix}
$$

> [!NOTE]
> Here we make sure the deviation in angular velocity is
> proportional to the time increment $\Delta t$ as the more time
> there is between sampling, the more uncertainty is involved in
> the samples.

$$
R = \begin{bmatrix}
  \sigma_{\theta}^2 & 0 \\
  0 & \sigma_{\phi}^2 \\
\end{bmatrix}
$$

We will tune the variances for $Q$ and $R$

$$
x_0 = \vec{0}
$$

But we will tune $P_0$

