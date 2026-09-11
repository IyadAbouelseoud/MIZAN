"""S0: JAX runs on CPU with x64 enabled and jax.grad matches an analytic derivative to 1e-12."""

from __future__ import annotations

import jax

jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp  # noqa: E402


def f(x):
    return jnp.sin(x) * jnp.exp(-(x**2) / 4.0) + x**3


def df_analytic(x):
    return (jnp.cos(x) - 0.5 * x * jnp.sin(x)) * jnp.exp(-(x**2) / 4.0) + 3.0 * x**2


def test_x64_enabled():
    assert jnp.ones(1).dtype == jnp.float64


def test_grad_matches_analytic():
    for x in (0.3, 1.7, -2.2):
        x = jnp.asarray(x)
        assert abs(float(jax.grad(f)(x)) - float(df_analytic(x))) < 1e-12
