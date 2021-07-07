import data as data

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import colorcet as cc
import matplotlib.patches as patches

level = ['Raw', 'FFT', 'Coherent', 'Microphonic']
color = ['k', 'cornflowerblue', 'orchid','yellowgreen']

cmap_ed = cc.cm.linear_tritanopic_krjcw_5_95_c24_r
cmap_diff = cc.cm.diverging_bwr_20_95_c54

def draw_noise_first(fig, channel, lvl):
    
    gs = gridspec.GridSpec(nrows=3, ncols=3, height_ratios=[1, 15, 6], hspace=0.25, wspace=0.25)
    
    ax  = []
    #0
    ax.append( fig.add_subplot(gs[1,0]) )
    im_i = ax[-1].imshow(data.data[lvl-1].transpose(), aspect = 'auto', cmap= cmap_ed, vmin=-5, vmax=25)
    ax[-1].set_title(level[lvl-1]+' Event')

    #1
    ax.append( fig.add_subplot(gs[1,1], sharey=ax[0], sharex=ax[0]))
    ax[-1].imshow(data.data[lvl].transpose(), aspect = 'auto', cmap= cmap_ed, vmin=-5, vmax=25)
    ax[-1].set_title(level[lvl]+'-Filtered Event')
    
    #2
    ax.append( fig.add_subplot(gs[0,0:2]) )
    cb = fig.colorbar(im_i, cax=ax[-1], orientation='horizontal')
    cb.ax.xaxis.set_ticks_position('top')
    cb.ax.xaxis.set_label_position('top')


    #3
    ax.append( fig.add_subplot(gs[1,2], sharey=ax[0], sharex=ax[0]))
    dr = data.data[lvl-1] - data.data[lvl]
    im_r = ax[-1].imshow(dr.transpose(), aspect = 'auto', cmap= cmap_diff, vmin=-2, vmax=2)
    ax[-1].set_title('Difference')

    #4
    ax.append(  fig.add_subplot(gs[0,2]) )
    cb = fig.colorbar(im_r, cax=ax[-1], orientation='horizontal')
    cb.ax.xaxis.set_ticks_position('top')
    cb.ax.xaxis.set_label_position('top')

    gsgs = gridspec.GridSpecFromSubplotSpec(1, 2, width_ratios=[9,2], subplot_spec=gs[2,:], wspace=0.02)

    #5
    ax.append( fig.add_subplot(gsgs[0,0]) )

    for l in range(lvl+1):
        ax[-1].plot(data.data[l, channel,:],c=color[l], label=level[l])

    ax[-1].set_xlabel('time bin')
    ax[-1].set_ylabel('ADC')
    ax[-1].set_xlim(0, 10000)
    ax[-1].text(0.05, 0.9, 'channel '+str(channel), transform=ax[-1].transAxes, fontsize=8)

    #6
    ax.append(  fig.add_subplot(gsgs[0,1]) )
    h,l = ax[-2].get_legend_handles_labels()
    ax[-1].legend(h,l, borderaxespad=0, bbox_to_anchor=(0.,1), loc="upper left")
    ax[-1].axis("off")

    plt.show()
    return ax


def draw_noise_update(fig, ax, channel, lvl):
    ax[1].imshow(data.data[lvl].transpose(), aspect = 'auto', cmap= cmap_ed, vmin=-5, vmax=25)

    dr = data.data[lvl-1] - data.data[lvl]
    ax[3].imshow(dr.transpose(), aspect = 'auto', cmap= cmap_diff, vmin=-2, vmax=2)

    ax[5].clear()
    for l in range(lvl+1):
        ax[5].plot(data.data[l, channel,:],c=color[l], label=level[l])
    ax[5].set_xlabel('time bin')
    ax[5].set_ylabel('ADC')
    ax[5].set_xlim(0, 10000)
    ax[5].text(0.05, 0.9, 'channel '+str(channel), transform=ax[5].transAxes, fontsize=8)
    fig.canvas.draw_idle()



def draw_hits(fig):
    pitch = 0.3125
    
    gs = gridspec.GridSpec(nrows=2, ncols=2, height_ratios=[1, 15], width_ratios=[2,1], hspace=0.25, wspace=0.1) 

    ax_v0 = fig.add_subplot(gs[1,0])
    ax_v1 = fig.add_subplot(gs[1,1])
    ax_col = fig.add_subplot(gs[0,:])
    
    hits_xz_v0 = [(h.X, h.Z) for h in data.evt_hits_list if h.view == 0]
    hits_q_v0  = [h.charge for h in data.evt_hits_list if h.view == 0]
    
    hits_xz_v1 = [(h.X, h.Z) for h in data.evt_hits_list if h.view == 1]
    hits_q_v1  = [h.charge for h in data.evt_hits_list if h.view == 1]
    
    box_v0 = [patches.Rectangle((h.X-pitch/2., h.Z_start), pitch,h.Z_stop-h.Z_start,linewidth=0.25,edgecolor='k',facecolor='none') for h in data.evt_hits_list if h.view == 0]
    
    box_v1 = [patches.Rectangle((h.X-pitch/2., h.Z_start), pitch,h.Z_stop-h.Z_start,linewidth=0.25,edgecolor='k',facecolor='none') for h in data.evt_hits_list if h.view == 1]
    
    im = ax_v0.scatter(*zip(*hits_xz_v0), c=hits_q_v0, cmap=cmap_ed, s=6, vmin=0., vmax=100.)
    for b in box_v0:
        ax_v0.add_patch(b)

         
    im = ax_v1.scatter(*zip(*hits_xz_v1), c=hits_q_v1, cmap=cmap_ed, s=6, vmin=0., vmax=100.)
    for b in box_v1:
        ax_v1.add_patch(b)


    cb = fig.colorbar(im, cax=ax_col, orientation='horizontal')
    cb.ax.xaxis.set_ticks_position('top')
    cb.ax.xaxis.set_label_position('top')
    
    ax_col.set_title('Charge Collected [fC]')
    
    ax_v0.set_ylabel('Z position [cm]')
    ax_v0.set_xlabel('X position [cm]')
    ax_v0.set_title('View 0')

    ax_v1.set_ylabel('Z position [cm]')
    ax_v1.set_xlabel('Y position [cm]')
    ax_v1.set_title('View 1')
    ax_v1.yaxis.tick_right()
    ax_v1.yaxis.set_label_position("right")
    plt.show()
    
def draw_2Dtracks(fig):
    import matplotlib as mpl
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=cc.glasbey_warm)

    gs = gridspec.GridSpec(nrows=1, ncols=2, width_ratios=[2,1], wspace=0.1) 

    ax_v0 = fig.add_subplot(gs[0,0])
    ax_v1 = fig.add_subplot(gs[0,1], sharey=ax_v0)
    #ax_col = fig.add_subplot(gs[0,:])

    ''' all hits '''
    hits_xz_v0 = [(h.X, h.Z) for h in data.evt_hits_list if h.view == 0]    
    hits_xz_v1 = [(h.X, h.Z) for h in data.evt_hits_list if h.view == 1]



    ''' all tracks '''
    track_xz_v0 = [[(p[0], p[1]) for p in t.path] for t in data.evt_trk2D_list if t.view==0]
    track_xz_v1 = [[(p[0], p[1]) for p in t.path] for t in data.evt_trk2D_list if t.view==1]
    
    ax_v0.scatter(*zip(*hits_xz_v0), c="#f5f0ef", s=6)
    for t in track_xz_v0:
        ax_v0.plot(*zip(*t))

    ax_v1.scatter(*zip(*hits_xz_v1), c="#f5f0ef", s=6)
    for t in track_xz_v1:
        ax_v1.plot(*zip(*t))
    ax_v0.set_ylabel('Z position [cm]')
    ax_v0.set_xlabel('X position [cm]')
    ax_v0.set_title('View 0')

    ax_v1.set_ylabel('Z position [cm]')
    ax_v1.set_xlabel('Y position [cm]')
    ax_v1.set_title('View 1')
    ax_v1.yaxis.tick_right()
    ax_v1.yaxis.set_label_position("right")
    plt.show()
    




def draw_3Dtracks(fig):
    import matplotlib as mpl
    from mpl_toolkits.mplot3d import Axes3D

    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=cc.glasbey_warm)

    gs = gridspec.GridSpec(nrows=2, ncols=2, height_ratios=[2,3], width_ratios=[2,1], wspace=0.1) 

    ax_v0 = fig.add_subplot(gs[0,0])
    ax_v1 = fig.add_subplot(gs[0,1], sharey=ax_v0)
    ax_3D = fig.add_subplot(gs[1,:], projection='3d')

    ''' all hits '''
    hits_xz_v0 = [(h.X, h.Z) for h in data.evt_hits_list if h.view == 0]    
    hits_xz_v1 = [(h.X, h.Z) for h in data.evt_hits_list if h.view == 1]



    ''' all 2D tracks '''
    track2D_xz_v0 = [[(p[0], p[1]) for p in t.path] for t in data.evt_trk2D_list if t.view==0]
    track2D_xz_v1 = [[(p[0], p[1]) for p in t.path] for t in data.evt_trk2D_list if t.view==1]

    ''' all 3D tracks (2D projection) '''
    track3D_xz_v0 = [[(p[0], p[2]) for p in t.path] for t in data.evt_trk3D_list if t.view==0]
    track3D_xz_v1 = [[(p[1], p[2]) for p in t.path] for t in data.evt_trk3D_list if t.view==1]

    
    ax_v0.scatter(*zip(*hits_xz_v0), c="#f5f0ef", s=6)
    for t in track2D_xz_v0:
        ax_v0.plot(*zip(*t), c='k', lw=0.5)

    for t in track3D_xz_v0:
        ax_v0.plot(*zip(*t), lw=3)

        
    ax_v1.scatter(*zip(*hits_xz_v1), c="#f5f0ef", s=6)
    for t in track2D_xz_v1:
        ax_v1.plot(*zip(*t), c='k', lw=0.5)


    for t in track3D_xz_v1:
        ax_v1.plot(*zip(*t), lw=3)


        
    ax_v0.set_ylabel('Z position [cm]')
    ax_v0.set_xlabel('X position [cm]')
    ax_v0.set_title('View 0')

    ax_v1.set_ylabel('Z position [cm]')
    ax_v1.set_xlabel('Y position [cm]')
    ax_v1.set_title('View 1')
    ax_v1.yaxis.tick_right()
    ax_v1.yaxis.set_label_position("right")



    ''' all 3D tracks (3D projection) '''
    track3D_xyz_v0 = [(p[0], p[1], p[2]) for t in data.evt_trk3D_list for p in t.path if t.view==0]
    track3D_xyz_v1 = [(p[0], p[1], p[2]) for t in data.evt_trk3D_list for p in t.path if t.view==1]
    

    ax_3D.scatter(*zip(*track3D_xyz_v0), c='#FBA120')
    ax_3D.scatter(*zip(*track3D_xyz_v1), c='#435497')

    ax_3D.set_xlim3d(-300, 300)
    ax_3D.set_ylim3d(0, 300)
    ax_3D.set_zlim3d(-30, 300)
    
    ax_3D.set_xlabel('View 0/X [cm]')
    ax_3D.set_ylabel('View 1/Y [cm]')
    ax_3D.set_zlabel('Drift/Z [cm]')


    ax_3D.grid(False)
    ax_3D.xaxis.pane.set_edgecolor('black')
    ax_3D.yaxis.pane.set_edgecolor('black')
    ax_3D.zaxis.pane.set_edgecolor('black')
    ax_3D.xaxis.pane.fill = False
    ax_3D.yaxis.pane.fill = False
    ax_3D.zaxis.pane.fill = False
    ax_3D.view_init(elev=22, azim=114)


    ax_3D.xaxis.set_major_locator(plt.MaxNLocator(3))
    ax_3D.yaxis.set_major_locator(plt.MaxNLocator(3))
    ax_3D.zaxis.set_major_locator(plt.MaxNLocator(4))
    

    ax_3D.xaxis._axinfo['tick']['inward_factor'] = 0.4
    ax_3D.xaxis._axinfo['tick']['outward_factor'] = 0.4
    ax_3D.yaxis._axinfo['tick']['inward_factor'] = 0.4
    ax_3D.yaxis._axinfo['tick']['outward_factor'] = 0.4
    ax_3D.zaxis._axinfo['tick']['outward_factor'] = 0.3
    ax_3D.zaxis._axinfo['tick']['inward_factor'] = 0.3
  
    
    
    plt.show()
    
   
