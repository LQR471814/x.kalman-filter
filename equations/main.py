import sympy as sp

dt = sp.symbols("dt")

xth, xph, bth, bph = sp.symbols("xth xph bth bph")

x = sp.Matrix(
    [
        [xth],
        [xph],
        [bth],
        [bph],
    ]
)

zth, zph = sp.symbols("zth zph")

z = sp.Matrix(
    [
        [zth],
        [zph],
    ]
)

H = sp.Matrix(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
    ]
)

F = sp.Matrix(
    [
        [1, 0, -dt, 0],
        [0, 1, 0, -dt],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
)

B = sp.Matrix(
    [
        [dt, 0],
        [0, dt],
        [0, 0],
        [0, 0],
    ]
)

wth, wph = sp.symbols("wth wph")

u = sp.Matrix([[wth], [wph]])

vwth, vwph, vbth, vbph = sp.symbols("vwth vwph vbth vbph")

Q = sp.diag(vwth**2 * dt**2, vwph**2 * dt**2, vbth**2, vbph**2)

vth, vph = sp.symbols("vth vph")

R = sp.Matrix(
    [
        [vth**2, 0],
        [0, vph**2],
    ]
)

P_prev = sp.Matrix(4, 4, lambda i, j: sp.symbols(f"P{i + 1}{j + 1}"))

x_p = F * x + B * u
P_p = F * P_prev * F.T + Q

K = P_p * H.T * (H * P_p * H.T + R).inv()
x = x_p + K * (z - H * x_p)
P = (sp.eye(4) - K * H) * P_p


# partial evaluation
def eval_const(expr):
    # dt = 20 ms
    # var(wth^2) = 1
    # var(wph^2) = 1
    # var(bth^2) = 1
    # var(bph^2) = 1
    # var(th) = 10
    # var(ph) = 10
    return (
        expr.subs(dt, sp.Rational(1, 10))
        .subs(vwth, 1)
        .subs(vwph, 1)
        .subs(vbth, 1)
        .subs(vbph, 1)
        .subs(vth, 10)
        .subs(vph, 10)
    )


x_p = eval_const(x_p)
P_p = eval_const(P_p)
K = eval_const(K)
x = eval_const(x)
P = eval_const(P)

print("x_p", x_p.shape)
print("P_p", P_p.shape)
print("K", K.shape)
print("x", x.shape)
print("P", P.shape)


def num_op(expr):
    add = 0
    mul = 0
    div = 0
    exp = 0

    for node in sp.preorder_traversal(expr):
        match node:
            case sp.Add():
                add += len(node.args) - 1
            case sp.Mul():
                for factor in node.args:
                    if isinstance(factor, sp.Pow) and factor.args[1].is_negative:
                        div += 1
                    else:
                        mul += 1
                mul -= 1
            case sp.Pow():
                if abs(node.args[1]) > 1:
                    exp += 1

    return (add, mul, div, exp)


add = 0
mul = 0
div = 0
exp = 0
for M in [x_p, P_p, K, x, P]:
    for expr in M:
        res = num_op(expr)
        add += res[0]
        mul += res[1]
        div += res[2]
        exp += res[3]

print(f"TOTAL OPS: + {add}, * {mul}, / {div}, ^ {exp}")

# assume ATmega328 processor, 32-bit fixed-point arithmetic using integers
# these are vague estimates
compute_cycles = 7 * add + 35 * mul + 200 * div
compute_time = compute_cycles / (16 * 10**6)

print(f"~{compute_time * 1000} ms")

