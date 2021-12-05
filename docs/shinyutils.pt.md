# shinyutils.pt module

Utilities for pytorch.


### _class_ shinyutils.pt.PTOpt(\*\*kwargs)
Wrapper around PyTorch optimizer and learning rate scheduler.

Usage:

```python
>>> opt = PTOpt(Adam, {"lr": 0.001})
>>> net = nn.Module(...)  # some network
>>> opt.set_weights(net.parameters())
>>> opt.zero_grad()
>>> opt.step()
```


#### _property_ optim_cls()
optimizer sub class


#### _property_ optim_params()
arguments for the optimizer


#### _property_ lr_sched_cls()
learning rate scheduler sub class


#### _property_ lr_sched_params()
arguments for the learning rate scheduler


#### set_weights(weights)
Set weights of underlying optimizer.


#### zero_grad()
Call `zero_grad` on underlying optimizer.


#### step()
Call `step` on underlying optimizer, and lr scheduler (if present).


#### _static_ add_help_args_to_parser(base_parser, group_title='pytorch help')
Add parser arguments for help on PyTorch optimizers and lr schedulers.


* **Parameters**


    * **base_parser** – `ArgumentParser` instance to add arguments to.


    * **group_title** – Title of a new group to add arguments to. If `None`, arguments
    are added to the base parser instead. Default is `"pytorch help"`.


Example:

```python
>>> arg_parser = ArgumentParser(
        add_help=False, formatter_class=corgy.CorgyHelpFormatter
)
>>> PTOpt.add_help_args_to_parser(arg_parser)
>>> arg_parser.print_help()
pytorch help:
  --explain-optimizer cls  describe arguments of a torch optimizer
                           (optional)
  --explain-lr-sched cls   describe arguments of a torch lr scheduler
                           (optional)
>>> arg_parser.parse_args(["--explain-optimizer", "Adamax"])
Adamax(params, lr=0.002, betas=(0.9, 0.999), eps=1e-08, weight_decay=0)
...
```


### _class_ shinyutils.pt.FCNet(\*\*kwargs)
Fully connected PyTorch network.


#### _property_ in_dim()
number of input features


#### _property_ out_dim()
number of output features


#### _property_ hidden_dims()
hidden layer dimensions


#### _property_ hidden_act()
activation function for hidden layers


#### _property_ out_act()
activation function for output layer


#### forward(x)
Forward a tensor through the network, and return the result.


* **Parameters**

    **x** – Input tensor of shape `(batch_size, in_dim)`.



### _class_ shinyutils.pt.NNTrainer(\*\*args)
Helper class for training a PyTorch model on a dataset.


#### _property_ iters()
number of training iterations


#### _property_ ptopt()
optimizer and learning rate scheduler


#### _property_ batch_size()
batch size for training


#### _property_ data_workers()
number of workers for loading data


#### _property_ shuffle_data()
whether to shuffle the dataset


#### _property_ pin_cuda()
whether to pin data to CUDA memory


#### _property_ drop_last()
whether to drop the last incomplete batch


#### _property_ pbar_desc()
description for training progress bar


#### set_dataset(value)
Set the training data.


* **Parameters**

    **value** – `torch.utils.data.Dataset` instance, or tuple of `torch.Tensor` or
    `np.ndarray` objects.



#### train(model, loss_fn, post_iter_hook=None)
Train a model.


* **Parameters**


    * **model** – Model (`nn.Module` instance) to train.


    * **loss_fn** – Loss function mapping input tensors to a loss tensor.


    * **post_iter_hook** – Optional callback function to call after each iteration.
    The function will be called with arguments
    `(iteration, x_batch, y_batch, yhat_batch, loss, pbar)`.



### _class_ shinyutils.pt.TBLogs(path=None)
TensorBoard logs type.


* **Parameters**

    **path** – Path to log directory. If `None` (default), a mock instance is
    returned.


Usage:

```python
tb_logs = TBLogs("tmp/tb")
tb_logs.writer  # `SummaryWriter` instance
TBLogs.mock  # mock instance
```


#### _class property_ mock()
Mock instace that no-ops for every call.
