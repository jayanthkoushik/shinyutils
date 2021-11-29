# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [10.0.0](https://github.com/jayanthkoushik/shinyutils/compare/v9.3.0...v10.0.0) (2021-11-29)


### ⚠ BREAKING CHANGES

* update `corgy` to version 2.4
* refactor `pt` to work better with `Corgy`
* make `MatWrap.mpl/plt/sns` properties
* replace `MatWrap.add_plotting_args` with `PlottingArgs` class
* disalbe auto calling `conf_logging` and add parse arguments for it
* remove logng.build_log_argp
* make arguments to conf_logging keyword only
* rename 'color' dependency group to 'colors'
* remove plotting and pytorch dependency groups
* increase minimum Python version to 3.9

### Features

* add helps for argparse arguments ([a2ccde1](https://github.com/jayanthkoushik/shinyutils/commit/a2ccde1d1569dc918f11de40f3e624b12329a413))
* make `MatWrap.mpl/plt/sns` properties ([bae2f78](https://github.com/jayanthkoushik/shinyutils/commit/bae2f78c3f5b53fd2119041bade4f07f7f76a5df))
* make arguments to conf_logging keyword only ([3b194d6](https://github.com/jayanthkoushik/shinyutils/commit/3b194d60982af83890c6161b24f6accb37dbb68e))
* refactor `pt` to work better with `Corgy` ([869be1c](https://github.com/jayanthkoushik/shinyutils/commit/869be1cf41d23766c56ddbb842a1ca83fa767ee4))
* replace `MatWrap.add_plotting_args` with `PlottingArgs` class ([3974414](https://github.com/jayanthkoushik/shinyutils/commit/397441490c559b094982e317d5394c52b64ce18e))


* disalbe auto calling `conf_logging` and add parse arguments for it ([aaaecbf](https://github.com/jayanthkoushik/shinyutils/commit/aaaecbf5fda9a133b2c405d2f5107971332f8a34))
* remove logng.build_log_argp ([94ea6b9](https://github.com/jayanthkoushik/shinyutils/commit/94ea6b974dde5f94f50ea1090956a152349bce32))


### build

* increase minimum Python version to 3.9 ([3e16baf](https://github.com/jayanthkoushik/shinyutils/commit/3e16baf41a5b7098f3fd8af714a98a85699c4e66))
* remove plotting and pytorch dependency groups ([729e781](https://github.com/jayanthkoushik/shinyutils/commit/729e781163ab5346d144b449ee4013de79dc6469))
* rename 'color' dependency group to 'colors' ([5d83afe](https://github.com/jayanthkoushik/shinyutils/commit/5d83afe2cc4e7e1668906262856aadc9627b99a4))
* update `corgy` to version 2.4 ([d67b369](https://github.com/jayanthkoushik/shinyutils/commit/d67b369d5dc74c0d701f4b668cd415c8e640a9db))

## [9.3.0](https://github.com/jayanthkoushik/shinyutils/compare/v9.2.1...v9.3.0) (2021-11-17)


### Features

* allow passing callback function to NNTrainer ([270a20b](https://github.com/jayanthkoushik/shinyutils/commit/270a20b093dff6b0e73e119513ca7f4143a948c4))

### [9.2.1](https://github.com/jayanthkoushik/shinyutils/compare/v9.2.0...v9.2.1) (2021-11-16)


### Bug Fixes

* update corgy to 2.0.1 ([b577e3b](https://github.com/jayanthkoushik/shinyutils/commit/b577e3b6adb00bd21aea5496dd62575909c727b7))

## [9.2.0](https://github.com/jayanthkoushik/shinyutils/compare/v9.1.0...v9.2.0) (2021-11-16)


### Features

* allow specifying palette size in matwrap ([b53e72b](https://github.com/jayanthkoushik/shinyutils/commit/b53e72bfed3b54cf80783f8e02042c6a4bfa9ca0))


### Bug Fixes

* update corgy to 2.0 for SubClassType update ([7a9e5b7](https://github.com/jayanthkoushik/shinyutils/commit/7a9e5b7b33253fc29db49d6cdf703543f258cbf1))

## [9.1.0](https://github.com/jayanthkoushik/shinyutils/compare/v9.0.0...v9.1.0) (2021-10-28)


### Features

* allow specifying custom backend directly in MatWrap ([cf8948d](https://github.com/jayanthkoushik/shinyutils/commit/cf8948d5969b1f1ebdf3ac2e04240ad00beb3b1c))


### Bug Fixes

* use actual colorblind cud palette ([8f34e19](https://github.com/jayanthkoushik/shinyutils/commit/8f34e19a272b1768a6116517982a3c9334d8d8c4))

## [9.0.0](https://github.com/jayanthkoushik/shinyutils/compare/v8.0.0...v9.0.0) (2021-10-21)


### ⚠ BREAKING CHANGES

* update dependencies

### Features

* add sh module ([43971aa](https://github.com/jayanthkoushik/shinyutils/commit/43971aad310b60544a38e07a998c6ac862ecb4f3))
* make matwrap.Plot save_file argument optional ([8f3da34](https://github.com/jayanthkoushik/shinyutils/commit/8f3da344e991f1d152210b7b6bc81ffe6f445a6b))


### build

* update dependencies ([0456a43](https://github.com/jayanthkoushik/shinyutils/commit/0456a43be86fc43c45dca8ceb72b72de5dd77bef))
