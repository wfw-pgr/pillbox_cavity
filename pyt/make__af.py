import numpy as np

# ========================================================= #
# ===  make__af.py ( for superfish )                    === #
# ========================================================= #

def make__af():

    # ------------------------------------------------- #
    # --- [1] load parameters                       --- #
    # ------------------------------------------------- #

    import nkUtilities.load__constants as lcn
    cnfFile = "dat/parameter.conf"
    const = lcn.load__constants( inpFile=cnfFile )

    # ------------------------------------------------- #
    # --- [2] comment & settings                    --- #
    # ------------------------------------------------- #

    if ( const["auto_drive_point"] ):
        unit_mm           = 1.e-3
        wavelength        = const["cv"] / const["frequency"]
        if ( const["auto_cell_Diameter"] ):
            Dp     = const["r1_bessel"] / np.pi * wavelength
        else:
            Dp     = const["cell_Diameter"]

        
        if ( const["add_beam_pipe"] ):
            const["xy_drive"] = [ const["L_beam_pipe"]/unit_mm, Dp*0.5 / unit_mm ]
        else:
            const["xy_drive"] = [ 0.0, Dp*0.5 / unit_mm ]
    
    comment = \
        "### {0} GHz Cavity\n"\
        "### pillbox-type cavity\n"\
        "### created by K.Nishida\n"\
        "###\n\n".format( const["frequency"] / 1.0e9 )

    generals   = \
        "kprob=1                              ! superfish problem \n"\
        "icylin=1                             ! cylindrical coordinates \n"\
        "conv={0}                             ! unit conversion ( e.g. cm => mm ) \n"\
        "freq={1}                             ! frequency (MHz) \n"\
        "dx={2}                               ! mesh size \n"\
        "xdri={3[0]},ydri={3[1]}              ! drive point of RF \n"\
        "kmethod=1                            ! use beta to compute wave number \n"\
        "beta={4}                             ! Particle velocity for transit-time integral\n"\
        .format( const["unit_conversion"], const["frequency"]/1.e6, const["meshsize"], \
                 const["xy_drive"], const["beta"] )

    boundaries = \
        "nbsup={0}                            ! boundary :: upper ( 0:Neumann, 1:Dirichlet )\n"\
        "nbslo={1}                            !          :: lower  \n"\
        "nbsrt={2}                            !          :: right  \n"\
        "nbslf={3}                            !          :: left   \n"\
        .format( const["boundary_upper"], const["boundary_lower"], \
                 const["boundary_right"], const["boundary_left"] )

    settings   = "&reg {0}{1}&\n\n".format( generals, boundaries )
    
    
    # ------------------------------------------------- #
    # --- [3] pillbox cavity geometry               --- #
    # ------------------------------------------------- #
    #  -- [3-1] preparation                         --  #
    wavelength = const["cv"] / const["frequency"]

    #  -- [3-2] Dp :: diameter of pillbox cavity    --  #
    if ( const["auto_cell_Diameter"] ):
        Dp     = const["r1_bessel"] / np.pi * wavelength
    else:
        Dp     = const["cell_Diameter"]
    
    #  -- [3-3] Lp :: length of pillbox cavity      --  #
    if ( const["auto_cell_Length"] ):
        Lp     = const["auto_cell_Lenfactor"] * wavelength
    else:
        Lp     = const["cell_Length"]

    #  -- [3-4] Message                             --  #
    print()
    print( "[make__af.py]   Lp  :: {0} ".format( Lp ) )
    print( "[make__af.py]   Dp  :: {0} ".format( Dp ) )
    print()

    #  -- [3-5] unit conversion for D & L           --  #
    unit_mm    = 1.e-3
    hDp        = 0.5 * Dp / unit_mm
    Lp         =       Lp / unit_mm
    rPipe      = const["r_beam_pipe"] / unit_mm
    LPipe      = const["L_beam_pipe"] / unit_mm

    # ------------------------------------------------- #
    # --- [4] write in a file                       --- #
    # ------------------------------------------------- #
    #  -- [4-1] make list (po) to write             --  #
    if ( const["add_beam_pipe"] ):
        pts        = [ [        0.0, 0.0   ],
                       [        0.0, rPipe ],
                       [   LPipe   , rPipe ],
                       [   LPipe   , hDp   ],
                       [   LPipe+Lp, hDp   ],
                       [   LPipe+Lp, rPipe ],
                       [ 2*LPipe+Lp, rPipe ],
                       [ 2*LPipe+Lp, 0.0   ],
                       [        0.0, 0.0   ],
        ]
    else:
        pts        = [ [ 0.0, 0.0 ],
                       [ 0.0, hDp ],
                       [  Lp, hDp ],
                       [  Lp, 0.0 ],
                       [ 0.0, 0.0 ] ]
    pts        = np.array( pts )

    #  -- [4-2] into SF $po format                  --  #
    z_, r_     = 0, 1
    geometry   = ""
    for ik, pt in enumerate( pts ):
        geometry += "$po x={0}, y={1} $\n".format( pt[z_], pt[r_] )

    #  -- [4-3] write in a file                     --  #
    with open( const["outFile"], "w" ) as f:
        f.write( comment  )
        f.write( settings )
        f.write( geometry )
    print()
    print( "[make__af.py] outFile :: {0} ".format( const["outFile"] ) )
    print()
    
    return()


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    make__af()
