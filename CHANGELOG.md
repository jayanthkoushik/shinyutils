# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [12.2.0](https://github.com/jayanthkoushik/shinyutils/compare/v12.1.1...v12.2.0) (2021-12-08)


### Features

* add `add_short_full_helps` argument to `run_prog` ([bc5c85b](https://github.com/jayanthkoushik/shinyutils/commit/bc5c85b0ca3cedfa4438f730004d6782b12bc1d7))
* add `run_prog` function ([fdae9ae](https://github.com/jayanthkoushik/shinyutils/commit/fdae9aef2773c83c52837cc97977e4b7f8ba71c7))
* add more arguments to `run_prog` ([20cd2bd](https://github.com/jayanthkoushik/shinyutils/commit/20cd2bdf392d819d995492a17c5fb5881fe30aa0))
* allow specifying sub-commands with keyword arguments in `run_prog` ([745b4f2](https://github.com/jayanthkoushik/shinyutils/commit/745b4f28e4a9a633ddca42f63616e9ed4c69e369))


### Bug Fixes

* apply `add_short_full_helps` to subparsers in `run_prog` ([df8392b](https://github.com/jayanthkoushik/shinyutils/commit/df8392be5681aa11222ae428fc463711e5653932))

### [12.1.1](https://github.com/jayanthkoushik/shinyutils/compare/v12.1.0...v12.1.1) (2021-12-07)


### Bug Fixes

* use Python 3.7 compatible type annotations ([24d033c](https://github.com/jayanthkoushik/shinyutils/commit/24d033c6f579805d8a963066629f9b2ea8ea3d20))

## [12.1.0](https://github.com/jayanthkoushik/shinyutils/compare/v12.0.0...v12.1.0) (2021-12-06)


### Features

* use `corgy 4.1` to support Python 3.7 and 3.8 ([6b367df](https://github.com/jayanthkoushik/shinyutils/commit/6b367df4a49f0f90c45eb340d6ccf10f1688d1b8))


### Bug Fixes

* fix mock `trange` implementation ([4b5d4a2](https://github.com/jayanthkoushik/shinyutils/commit/4b5d4a20da5580703ff632bec8968c39410290ac))

## [12.0.0](https://github.com/jayanthkoushik/shinyutils/compare/v11.0.0...v12.0.0) (2021-12-05)


### ⚠ BREAKING CHANGES

* update `corgy` to version 4.0
* simplify `NNTrainer` var names
* refactor `pt` based on latest `corgy`

### Features

* call `MatWrap.configure` in `PlottingArgs.__init__` ([d7c1628](https://github.com/jayanthkoushik/shinyutils/commit/d7c1628c1c975cb86d455c5607e1163e54b8c728))
* mark wrapped names in `matwrap` as `Any` so `mypy` doesn't complain ([bf8c586](https://github.com/jayanthkoushik/shinyutils/commit/bf8c5866a7267f098e83c3a86818f6e32dc7956a))
* refactor `pt` based on latest `corgy` ([d9123e2](https://github.com/jayanthkoushik/shinyutils/commit/d9123e2c034ed323948e71558457449e54b2b74a))
* simplify `NNTrainer` var names ([7bf49d4](https://github.com/jayanthkoushik/shinyutils/commit/7bf49d4f7120867d0e2dd73c37e1ee76028436ea))


### Bug Fixes

* fix wrapped name import from `matwrap` ([ef4faae](https://github.com/jayanthkoushik/shinyutils/commit/ef4faae34bdf4b47ff732911f29ccb3b3b06f16f))


### build

* update `corgy` to version 4.0 ([d72b8d7](https://github.com/jayanthkoushik/shinyutils/commit/d72b8d78614dd52c142faaff4f6482d8f02afbf7))

## [11.0.0](https://github.com/jayanthkoushik/shinyutils/compare/v10.0.0...v11.0.0) (2021-12-02)


### ⚠ BREAKING CHANGES

* update to `corgy 3.1`

### Features

* add `py.typed` to inform type checkers about annotations ([2451394](https://github.com/jayanthkoushik/shinyutils/commit/245139443c38cac4747598e44dcafe5dd3d6ffa1))


### build

* update to `corgy 3.1` ([3a0526f](https://github.com/jayanthkoushik/shinyutils/commit/3a0526f96af9daffe3182d28389efef5ad3cdb51))

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
