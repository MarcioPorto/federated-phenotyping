import torch
import numpy as np

from tqdm import tqdm

def _get_trainable_params(model):
    """Get Parameters with `requires.grad` set to `True`"""
    trainable_params = []
    for x in model.parameters():
        if x.requires_grad:
            trainable_params.append(x)
    return trainable_params

def _get_lr(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']

def calc_results(predictions, labels):
    predictions = (predictions > 0.5).float()
    mask = (predictions == labels).foat()
    correct = mask.sum(dim = 0)
    return correct


def _train_model(model, train_loader, epoch, num_epochs, optimizer, criterion, writer, current_lr, log_every=100):
    
    # Set to train mode
    model.train()

    
    correct = torch.zeros(1023).cuda()
    correct = correct.float()
    
    total = 0.

    losses = []

    for i, (patients, labels) in enumerate(train_loader):
        optimizer.zero_grad()

        if torch.cuda.is_available():
            patients = patients.cuda()
            labels = labels.cuda()

        output = model(patients)

        loss = criterion(output, labels)
        loss.backward()
        optimizer.step()

        loss_value = loss.item()
        losses.append(loss_value)

        output = torch.sigmoid(output)
        cor = calc_results(output, labels)
        correct += cor
        total += labels.size(0)

        if (i % log_every == 0):
            print("[Epoch: {0} / {1} | Batch : {2} / {3} ]| Train Loss {4} | Train Acc : {5} | lr : {6}".format(
                      epoch + 1,
                      num_epochs,
                      i,
                      len(train_loader),
                      np.round(np.mean(losses), 4),
                      torch.mean(correct / (total + 1e-8)),
                      current_lr)
                    )
    
    print(correct, total)

    train_loss_epoch = np.round(np.mean(losses), 4)
    train_acc_epoch = torch.mean(correct / (total + 1e-8))

    print(correct.min())

    return train_loss_epoch, train_acc_epoch

def _eval_model(model, val_loader, epoch, num_epochs, criterion, writer, current_lr, log_every=100):
    
    # Set to train mode
    model.eval()

    print('validating model...')

    correct = torch.zeros(1023).cuda()
    correct = correct.float()
    
    total = 0.

    losses = []

    for i, (patients, labels) in tqdm(enumerate(val_loader)):

        if torch.cuda.is_available():
            patients = patients.cuda()
            labels = labels.cuda()

        with torch.no_grad():
            output = model(patients)
            loss = criterion(output, labels)

        loss_value = loss.item()
        losses.append(loss_value)

        output = torch.sigmoid(output)
        cor = calc_results(output, labels)
        correct += cor
        total += labels.size(0)

    val_loss_epoch = np.round(np.mean(losses), 4)
    val_acc_epoch = torch.mean(correct / (total + 1e-8))

    return val_loss_epoch, val_acc_epoch