include("./ising.jl")

function bench()
    J = 1.
    T = 2.27

    L = 100
    sweeps = 10000

    spin = Array{Int8, 2}(L, L)
    for i = 1:L
        for j = 1:L
            spin[i,j] = 1
        end
    end
    energies = Array{Float64}(sweeps+1)
    tot_magnetization = Array{Int64}(sweeps+1)
    save_every_nth = 1
    seed = 0
    lat = Lattice(spin, L, 0, 0, 0)

    solve(lat, sweeps, J, T, energies, tot_magnetization, save_every_nth, seed)
end

@time bench()
