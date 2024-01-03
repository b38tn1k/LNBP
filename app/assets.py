from flask_assets import Bundle

common_css = Bundle(
    'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css',
    'css/vendor/helper.css',
    'css/main.css',
    'css/overrides.css',
    filters='cssmin',
    output='public/css/common-1.css'
)

common_js = Bundle(
    'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js',
    Bundle(
        'js/main.js',
        filters='jsmin'
    ),
    output='public/js/common-2.js'
)


# common_css = Bundle(
#     'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css',
#     'css/vendor/helper.css',
#     'css/main.css',
#     'css/overrides.css',
#     filters='cssmin',
#     output='public/css/common-1.css'
# )

# common_js = Bundle(
#     'https://code.jquery.com/jquery-3.2.1.slim.min.js',
#     'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
#     'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js',
#     Bundle(
#         'js/main.js',
#         filters='jsmin'
#     ),
#     output='public/js/common-2.js'
# )

store_css = Bundle(
    'css/store.css',
    filters='cssmin',
    output='public/css/store.css'
)

landing_css = Bundle(
    'css/landing.css',
    filters='cssmin',
    output='public/css/landing.css'
)

tabler_css = Bundle(
    # 'https://rawcdn.githack.com/Sumukh/Ignite/70bf953851a356e785528b56ca105042074a3d5a/appname/static/tabler/css/dashboard.css',
    # 'css/rawcdn_github_backup.css',
    # 'css/rawcdn_github_backup_inv.css',
    'css/rawcdn_github_backup_inv_brightened.css',
    'css/overrides.css',
    filters='cssmin',
    output='public/css/tabler.css'
)

tabler_js = Bundle(
    'tabler/js/vendors/jquery-3.2.1.min.js',
    # 'tabler/js/vendors/bootstrap.bundle.min.js',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js',
    'tabler/js/vendors/circle-progress.min.js',
    'tabler/js/vendors/selectize.min.js',
    'tabler/js/vendors/jquery.tablesorter.min.js',
    'tabler/js/core.js',
    
    output='public/js/tabler.js'
)

tabler_plugins_css = Bundle(
    'tabler/js/plugins/charts-c3/plugin.css',
    output='public/css/tabler-plugins.css'
)

tabler_plugins_js = Bundle(
    'tabler/js/vendors/chart.bundle.min.js',
    'tabler/js/vendors/jquery.sparkline.min.js',
    'tabler/js/vendors/jquery-jvectormap-2.0.3.min.js',
    'tabler/js/vendors/jquery-jvectormap-de-merc.js',
    'tabler/js/vendors/jquery-jvectormap-world-mill.js',
    'tabler/js/plugins/charts-c3/js/d3.v3.min.js',
    'tabler/js/plugins/charts-c3/js/c3.min.js',
    'tabler/js/plugins/input-mask/js/jquery.mask.min.js',
    # Other Plugins as needed.
    output='public/js/tabler-plugins.js'
)

scheduler_js = Bundle(
    "https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.min.js",
    'js/league_scheduler/info_div_handler_class.js',
    'js/league_scheduler/dragula_drop_actions.js',
    'js/league_scheduler/flight_tab_setup.js',
    'js/league_scheduler/dragula_legend_controls.js',
    'js/league_scheduler/dragula_drop_logic.js',
    'js/league_scheduler/dragula_config.js',
    'js/league_scheduler/save_button.js',
    
    filters='jsmin',

output='public/js/scheduler.js'
)