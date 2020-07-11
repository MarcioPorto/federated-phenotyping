import torch
from dataset import Patient
from model import pat_embed
from config import config
from torch.utils.tensorboard import SummaryWriter
import time

from utils import _train_model, _eval_model, _get_lr


from torch.utils import data

model = pat_embed(path + '/pretrained_cuis.npy')
if torch.cuda.is_available():
        model = model.cuda()

path = '../../../required files/Training files'

train_data = Patient(path + '/train_pat.txt', 
                    path + '/cui2idx.pt', 
                    path + '/label2idx.pt',
                    path + '/valid_cuis.txt',
                    path + '/cuis/', # Folder where extracted patient cuis are
                    path + '/labels/')  # Folder where patient labels are

val_data = Patient(path + '/val_pat.txt', 
                    path + '/cui2idx.pt', 
                    path + '/label2idx.pt',
                    path + '/valid_cuis.txt',
                    path + '/cuis/', # Folder where extracted patient cuis are
                    path + '/labels/')  # Folder where patient labels are

train_loader = data.DataLoader(train_data, batch_size=50, num_workers=6, shuffle=True)
val_loader = data.DataLoader(val_data, batch_size=50, num_workers=6, shuffle=False)

print('Initializing Loss Method...')
criterion = torch.nn.BCEWithLogitsLoss()
val_criterion = torch.nn.BCEWithLogitsLoss()

if torch.cuda.is_available():
        criterion = criterion.cuda()
        val_criterion = val_criterion.cuda()

print('Setup the Optimizer')
optimizer = torch.optim.RMSprop(model.parameters(), lr=config['lr'], weight_decay=config['weight_decay'])

scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, patience=3, factor=.3, threshold=1e-4, verbose=True)

starting_epoch = config['starting_epoch']
num_epochs = config['max_epoch']
log_train = config['log_train']
log_val = config['log_val']

writer = SummaryWriter(comment='lr={} task={}'.format(config['lr'], config['task']))
t_start_training = time.time()

for epoch in range(starting_epoch, num_epochs):

    current_lr = _get_lr(optimizer)
    epoch_start_time = time.time()  # timer for entire epoch

    train_loss, train_acc = _train_model(
        model, train_loader, epoch, num_epochs, optimizer, criterion, writer, current_lr, log_train)

    val_loss, val_acc = _eval_model(
        model, val_loader,  epoch, num_epochs, val_criterion, writer, current_lr, log_val)

    writer.add_scalar('Train/Avg Loss', train_loss, epoch)
    writer.add_scalar('Val/Avg Loss', val_loss, epoch)

    scheduler.step(val_loss)

    t_end = time.time()
    delta = t_end - epoch_start_time

    print("train loss : {0} | train acc {1} | val loss {2} | val acc {3} | elapsed time {4} s".format(
        train_loss, train_acc.item(), val_loss, val_acc.item(), delta))

    print('-' * 30)

    writer.flush()

    # if bool(config['save_model']):
    #     file_name = 'model_{}_{}_val_auc_{:0.4f}_train_auc_{:0.4f}_epoch_{}.pth'.format(config['exp_name'], config['task'], val_auc, train_auc, epoch+1)
    #     torch.save({
    #         'model_state_dict': model.state_dict()
    #     }, './weights/{}/{}'.format(config['task'],file_name))

t_end_training = time.time()
print(f'training took {t_end_training - t_start_training} s')
writer.flush()
writer.close()