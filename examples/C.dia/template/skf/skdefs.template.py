atomconfigs = {
    "C": AtomConfig(
        znuc=6,
        mass=12.011,
        occupations=[
            [ [ 1.0, 1.0 ], [ 1.0, 1.0 ], ],  # s
            [               [ 1.0, 1.0 ], ],  # p
            ],
        valenceqns=[
            [2, ],  # s
            [2, ],  # p
            ],
        relativistic=True,
        orbitalresolved=True,
        ),

    "C1": AtomConfig( # 3s-star
        znuc=6,
        mass=12.011,
        occupations=[
            [ [ 1.0, 1.0 ], [ 1.0, 1.0 ], [ 1.0, 1.0 ], ],   # s
            [               [ 1.0, 1.0 ]],  # p
            ],
        valenceqns=[
            [3, ],  # s
            [2, ],  # p
        ],
        relativistic=True,
        orbitalresolved=True,
        # override the 3s onsite (n=3,L=0); n counts from 1, L from 0
        #override_onsite={ (3, 0): (E3s)f },
        ),
}

skbases = {
    "C": SlaterBasis(
        exponents=[
        # Geometric progression, very similar to the one used in PBC
            [0.4,    0.787,  1.549,  3.049,  6.], # s
            [0.4,    0.787,  1.549,  3.049,  6.], # p
            ],
        maxpowers= [
            2,  # s
            2,  # p 
            ]
        ),

    "C1": SlaterBasis(
        exponents=[
        # Geometric progression, very similar to the one used in PBC
            [0.4,    0.787,  1.549,  3.049,  6.], # s
            [0.4,    0.787,  1.549,  3.049,  6.], # p
            ],
        maxpowers= [
            2,  # s
            2,  # p 
            ]
        ),
}

compressions = {
    "C": Compression(
        potcomp="potential",
        potcomp_parameters= [ (2, %(R0)f), # s
                              (2, %(R0)f), # p
                            ],
        wavecomp="potential",
        wavecomp_parameters=[ (2, %(R0)f), # s
                              (2, %(R0)f), # p
                            ],
        ),

    "C1": Compression(
        potcomp="potential",
        potcomp_parameters= [ (2, %(R0)f), # s
                              (2, %(R0)f), # p
                            ],
        wavecomp="potential",
        wavecomp_parameters=[ (2, %(R0)f), # s
                              (2, %(R0)f), # p
                            ],
        ),
} 