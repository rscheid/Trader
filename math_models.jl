# Julia Monte-Carlo-Simulation
function monte_carlo(prices::Vector{Float64}, steps::Int, mu::Float64, sigma::Float64)
    simulation = Float64[prices[end]]  # Start mit dem letzten Preis
    for _ in 1:steps
        drift = mu - 0.5 * sigma^2
        shock = sigma * randn()
        next_price = simulation[end] * exp(drift + shock)
        push!(simulation, next_price)
    end
    return simulation
end
