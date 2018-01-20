function wraparound(i, offset, len)
  return ((len + (i-1 + offset)) % len)+1
end

mutable struct Lattice
    Spin::Array{Int8, 2}    # spin values (may be +1 or -1)
    L::Int                  # dimension of lattice
    Energy::Float64
    Tot_magnetization::Int64
    Accepted_configurations::Int64
end

function find_energy(lat::Lattice, J)
    L = lat.L
    A = lat.Spin

    E = 0
    for i = 1:L
        for j = 1:L
            E += A[i,j] * A[wraparound(i, 1, L), j] # horizontal neighbour
            E += A[i,j] * A[i, wraparound(j, 1, L)] # vertical neighbour
        end
    end
    lat.Energy = -J*E
end

function find_tot_magnetization(lat::Lattice)
    L = lat.L
    A = lat.Spin

    tot_magnetization = 0
    for i = 1:L
        for j = 1:L
            tot_magnetization += A[i,j]
        end
    end

    lat.Tot_magnetization = tot_magnetization
end

function relative_change_of_energy(lat::Lattice, i::Int, j::Int)
    L = lat.L
    A = lat.Spin

    E_old_down =    A[i,j] * A[wraparound(i,1,L),  j]
    E_old_up =      A[i,j] * A[wraparound(i,-1,L), j]
    E_old_right =   A[i,j] * A[i, wraparound(j,1,L) ]
    E_old_left =    A[i,j] * A[i, wraparound(j,-1,L)]
    E_old = E_old_right + E_old_left + E_old_up + E_old_down

    #=
    the difference in energy is equal to
            dE = -J * (E_new - E_old)
    Since the change consists of flipping the sign of A[i][j],
            E_new = -E_old
    Implying
            dE = -J * (- 2 * E_old) = 2*J*E_old
    Since, only the relative value (scaled by a positive factor) is of
    importance, it is sufficient to return E_old
    =#
    return E_old
end

function metropolis(lat::Lattice, sweeps::Int64, J::Float64, energies::Array{Float64},
    tot_magnetization::Array{Int64}, r::MersenneTwister, dE_cache::Array{Float64},
    save_every_nth::Int64)
    L = lat.L
    spin = lat.Spin
    accepted_configurations = 0

    for sweep = 1:sweeps
        for count = 0:L*L
            pos_1d = rand(r, 0:L*L-1)
            i = div(pos_1d, L) + 1
            j = (pos_1d % L) + 1

            relative_dE = relative_change_of_energy(lat, i, j)
            dE = dE_cache[5+relative_dE]
            ran = rand(r, Float64)

            if dE > ran
                # ACCEPT
                spin[i,j] *= -1
                lat.Energy += 2*J*relative_dE
                lat.Tot_magnetization += 2*spin[i,j]
                accepted_configurations += 1
            end

        end

        if (sweep % save_every_nth) == 0
            energies[div(sweep, save_every_nth)] = lat.Energy
            tot_magnetization[div(sweep, save_every_nth)] = lat.Tot_magnetization
        end
    end

    lat.Accepted_configurations = accepted_configurations
end

function solve(lat::Lattice, sweeps::Int64, J::Float64, T::Float64,
    energies::Array{Float64}, tot_magnetization::Array{Int64}, save_every_nth::Int64,
    seed)
    beta = 1 / T

    find_energy(lat, J)
    find_tot_magnetization(lat)

    dE_cache = Array{Float64}(9)
    for i = 1:2:9
        dE_cache[i] = exp(-beta*2*(i-4))
    end

    # create new RNG
    r = MersenneTwister(seed)

    metropolis(lat, sweeps, J, energies, tot_magnetization, r, dE_cache,
                save_every_nth)
end
