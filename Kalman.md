### Purpose

The purpose of the Kalman Filter is to take multiple potentially
noisy sources of information about the state of a system and a
deterministic model of a system to construct the most optimal (in
the least-squares mean sense) estimate for the state of the
system.

> **Example**
>
> You have a gyroscope (tells you rotational velocity) and
> accelerometer (tells you absolute rotation). You are not
> confident in the measurements of the accelerometer and want to
> factor in the information you gain from the gyroscope to
> construct a better estimate for the true orientation of the
> device.

### Components

- $x$ - "State vector"
- $F$ - "State transition model"
    - This is a matrix that transform the current state vector
      into the next state following a deterministic set of rules.
    - Ex. Newton's laws of motion.
- $z$ - "Measurements vector"
- $H$ - "Observation model"
    - This is a matrix that transforms a vector from state space
      to measurement space.
    - In other words, it converts a state into the measurement
      that would have arose from that state.
- $P$ - "Estimate covariance"
    - This is a matrix that tracks the uncertainty in the
      estimated state.
    - More details on this in a later section.
- $Q$ - "Process noise covariance"
    - This is a matrix that tracks the uncertainty in system
      dynamics ($F$).
    - Ex. A truck moving along on the road will experience all
      sorts of random accelerations due to bumps and etc...
- $R$ - "Measurement noise covariance"
    - This is a matrix that tracks the uncertainty in
      measurements.
    - Ex. GPS usually has an error of $\pm 3\ \text{m}$.
- $u$ (optional) - "Control input"
- $B$ (optional) - "Control input model"
    - A matrix that models deterministic effects for a given
      control input on the system.
    - Ex. The reorientation of a servo in response to a change in
      angle.
- $K$ - "Kalman gain"
    - This is a matrix that is derived from all the other
      components that represents how much we trust our own
      predictions based on prior state and the deterministic model
      vs. how much we trust the measurements.
    - It also describes how much weight to put towards our
      predictions and the measurements to compute our best
      estimate for the current state.
- Prediction: Processes for predicting the system state.
- Update: Processes for updating your prediction methods based on
  how well your predictions performed.

### Details on Covariance Matrices

Any covariance matrix tracks uncertainty across the variables of a
random vector.

- On the diagonals of the matrix is the variance in each state
  vector variable.
- On the off-diagonals is the covariance of each vector variable
  with the other vector variables.

Example, for state vector:

$$
x = \begin{bmatrix}
  a \\ b
\end{bmatrix}
$$

The estimate covariance matrix gives the uncertainty of $x$:

$$
P = \begin{bmatrix}
  1 & 2 \\
  2 & 3
\end{bmatrix}
$$

- The variance for $a$ is $1$ and variance for $b$ is $3$.
    - So the amount of uncertainty in $a$ is $1$.
    - The amount of uncertainty in $b$ is $3$.
    - For a more complete idea of what this "uncertainty" actually
      is, look [here](https://en.wikipedia.org/wiki/Variance).
- $\text{cov}(a,b) = 2$
    - Describes how much $a$ and $b$ are coupled together.
    - This is not necessarily good or bad, it depends on context.
        - If $a$ and $b$ are supposed to be highly coupled with
          regard to the system, then this is a good sign.
        - If they are not, then this is not a good sign.
        - Ex. High covariance between angles in the case for an
          accelerometer+gyroscope is a bad sign if the thing is
          supposed to be able to rotate freely.

> [!NOTE]
> Since $\text{cov}$ doesn't depend on order, $\text{cov}(a,b) = \text{cov}(b,a)$.
> As such, the matrix must be symmetric along the diagonal.

Since these are properties that apply to all covariance matrices,
the matrix $R$ would have the same properties.

### Covariance

Covariance is simply the amount that two random variables "vary
together".

- For $\text{cov}(x, y) > 0$: The amount greater values of $x$
  correspond to greater values of $y$ and lesser values of $x$ for
  lesser values of $y$.
- For $\text{cov}(x, y) < 0$: Greater $x$ is correlated with
  lesser $y$ and vice versa
- For $\text{cov}(x, y) = 0$: The two values are independent of
  each other.

For scalar values, covariance is defined as such:

$$
\text{cov}(x, y) = \mathbb{E}[(x - \mathbb{E}[x])(y - \mathbb{E}[y])]
$$

> [!NOTE]
> $\mathbb{E}$ simply means the expected value of the expression
> in the parenthesis (square or not).

Extending this definition for random vectors $\eta$ is as such:

$$
\text{cov}(\eta) = \mathbb{E} [(\eta - \mathbb{E}[\eta])(\eta - \mathbb{E}[\eta])^T]
$$

Suppose

$$
\eta = \begin{bmatrix} x \\ y \end{bmatrix}
$$

Where

$$
\mathbb{E}(\eta) = \begin{bmatrix} 0 \\ 0 \end{bmatrix}
$$

Thus

$$
\text{cov}(\eta) = \mathbb{E}(\eta \eta^{T})
$$

$$
\text{cov}(\eta) = \mathbb{E} \begin{bmatrix}
  \eta_1^2 & \eta_1 \eta_2 \\
  \eta_2 \eta_1 & \eta_{2}^2
\end{bmatrix}
$$

$\eta_{k}^2$ is the squared distance from the mean (0), thus the
expected value of $n_{k}^2$ is the **variance**.

$\eta_1 \eta_2$ is the product of the two variables' distances
from the mean, thus the expected value of $\eta_1 \eta_2$ is the
**covariance**.

So

$$
\text{cov}(\eta) = \mathbb{E} \begin{bmatrix}
  \text{var}(\eta_1) & \text{cov}(\eta_1, \eta_2) \\
  \text{cov}(\eta_2, \eta_1) & \text{var}(\eta_2)
\end{bmatrix}
$$

### Details on Process Noise Covariance

The process noise covariance $Q$ is a covariance matrix for
expected uncertainty in our deterministic model of the system $F$.

Example: A truck moving along the road at constant velocity
experiencing random accelerations.

Let's say our system is defined as:

$$
x = \begin{bmatrix}
p \\ v
\end{bmatrix}
$$

Where $p$ is position and $v$ is velocity.

$$
F = \begin{bmatrix}
1 & 1 \\ 0 & 1
\end{bmatrix}
$$

You can compute $Fx$ to see that $p_{k+1} = p_{k} + v_{k}$ and
$v_{k+1} = v_{k}$.

Remember the definition for covariance matrix.

$$
Q = \text{cov}(\eta) = \mathbb{E} [(\eta - \mathbb{E}[\eta])(\eta - \mathbb{E}[\eta])^T]
$$

Where $\eta$ is the vector of process noise contributions to the
state.

So in our example it would be:

$$
\eta = \begin{bmatrix}
  \frac{1}{2}\Delta t^{2} a \\
  \Delta t a
\end{bmatrix}
$$

We assume mean random acceleration is $\vec{0}$.

So

$$
Q = \mathbb{E}(\eta \eta^T)
$$

Remember Newton's laws of motion $x = x_0 + v_{i} t + \frac{1}{2} at^{2}$,
$v_{f} = v_{i} + at$.

We do matrix multiplication.

$$
\eta \eta^T = \begin{bmatrix}
\frac{1}{4}\Delta t^{4} a^{2} & \frac{1}{2}\Delta t^{3} a^{2} \\
\frac{1}{2}\Delta t^{3} a^{2} & \Delta t^{2} a^{2} \\
\end{bmatrix}
$$

Remember $\mathbb{E}(a^2) = \sigma^2$ ($\sigma^2$ is the
variance).

$$
Q = \sigma^2 \begin{bmatrix}
  \frac{1}{4}\Delta t^2 & \frac{1}{2} \Delta t^3 \\
  \frac{1}{2} \Delta t^3 & \Delta t^2
\end{bmatrix}
$$

If we assume we will be sampling in $\Delta t = 1$ increments and
$\sigma^2 = 2$ (arbitrary tuned value).

$$
Q = \begin{bmatrix}
  0.5 & 1 \\
  1 & 2
\end{bmatrix}
$$

### Prediction equations

I won't attempt to explain why these equations are the way they
are because the maths are beyond me and I don't have the time as
of now. ):

The equation for predicting the next state based on model, current
state, and optional control input.

$$
x_{k|k-1} = Fx_{k-1|k-1} + Bu_{k}
$$

The equation for predicting the estimation covariance (how much we
trust the prediction) based on model and process noise.

$$
P_{k|k-1} = FP_{k-1|k-1} F^{T} + Q
$$

### Update equations

The equation for computing Kalman Gain (how much weight to give
measurements vs. prediction).

$$
K_{k} = P_{k|k-1} H^{T} (HP_{k|k-1} H^{T} + R)^{-1}
$$

The equation for computing the best estimate for the current state
based on measurements and prediction.

$$
x_{k|k} = x_{k|k-1} + K_{k}(z_{k} - Hx_{k|k-1})
$$

The equation for updating the estimation covariance (how much we
trust the prediction) based on Kalman Gain and predicted
estimation covariance.

$$
P_{k|k} = (I-K_{k} H) P_{k|k-1}
$$

> [!NOTE]
> $I$ is the identity matrix.

### Tuning

Of the components of the Kalman Filter, you are really only responsible for
tuning:

- $Q$ - The process noise covariance.
    - You would usually derive an equation for computing this
      matrix according to deterministic rules. See "Details on
      Process Noise Covariance", then precompute the matrix
      according to constants like $\Delta t$ and tune a value for
      $\sigma^2$ (variance).
- $R$ - The measurement noise covariance.
    - You would usually consult the sensor specs on error for
      computing this matrix.
    - Ex. GPS has a typical error of $\pm 3\ \text{m}$ so its
      variance along each coordinate would be $9$. (the expected
      squared error)
- $x_0$ - The initial state.
    - Reasonable guess, the state estimate will correct itself
      over time.
- $P_0$- The initial estimate covariance matrix.
    - This should reflect your certainty of the initial state.
    - If you are confident in your guess on the initial state, set
      the variance low.
    - If you only have a rough guess, set the variance high.
    - If you don't know what values to set for covariance, just
      set it to zero.

