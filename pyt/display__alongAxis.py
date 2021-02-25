import sys
import numpy                      as np
import nkUtilities.load__config   as lcf
import nkUtilities.plot1D         as pl1
import nkUtilities.configSettings as cfs


# ========================================================= #
# ===  display                                          === #
# ========================================================= #
def display():
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    config  = lcf.load__config()
    datFile = "dat/superfish.dat"
    pngFile = "png/alongAxis.png"

    # ------------------------------------------------- #
    # --- [2] Fetch Data                            --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    Data  = lpf.load__pointFile( inpFile=datFile, returnType="point" )
    eps   = 1.e-8
    val   = 1.e-3
    index = np.where( np.abs( Data[:,1] -val ) <= eps  )
    Data  = Data[index][:]
    xAxis = Data[:,0] - 0.5*( Data[0,0] + Data[-1,0] )
    Ez    = Data[:,3] * 1.e-6
    Er    = Data[:,4] / ( val * 100.0 ) * 1.e-6
    # Hp    = Data[:,6] / ( val * 100.0 )
    
    # ------------------------------------------------- #
    # --- [3] config Settings                       --- #
    # ------------------------------------------------- #
    cfs.configSettings( configType="plot1D_def", config=config )
    config["FigSize"]        = (4,4)
    config["yTitle"]         = "Ez (MV/m), Er/r (MV/m/cm)"
    config["xTitle"]         = "Z (m)"
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xRange"]     = [-0.0,+0.05]
    config["plt_yRange"]     = [-0.0,+3.0]
    config["plt_linewidth"]  = 1.8
    config["xMajor_Nticks"]  = 6
    config["yMajor_Nticks"]  = 4

    # ------------------------------------------------- #
    # --- [4] plot Figure                           --- #
    # ------------------------------------------------- #
    fig = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=xAxis, yAxis=Er, label="Er/r" )
    fig.add__plot( xAxis=xAxis, yAxis=Ez, label="Ez" )
    # fig.add__plot( xAxis=xAxis, yAxis=Hp, label="Hp" )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    display()

