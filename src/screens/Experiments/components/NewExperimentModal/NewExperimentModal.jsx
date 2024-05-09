import * as React from 'react';
import Box from '@mui/material/Box';
import { Button } from "../../../../components/Button";
import { ModalFooterItem } from "../ModalFooterItem";
import {CreateForms} from "../CreateForms";
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';

import './style.css';
import { useNavigate } from 'react-router-dom';



export function NewExperimentModal({ blank, onSaveClick = ()=>{} }) {
  let navigate= useNavigate();
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const handleButtonClick = (id) => {
    if(id==0){
      handleClose();
    }else{
      onSaveClick();
    }
  }
  return (
    <div >
      <Button
          buttonText="New experiment"
          className={blank ? "button-instance-blank" : "button-instance"}
          iconClassName="design-component-instance-node"
          size="large"
          stateProp="enabled"
          type="text-icon"
          onClick={handleOpen}
          style={"primary"}
          isModal={true}
        />
      <div className="content">
        <div className="slot">
          <Modal
            open={open}
            onClose={handleClose}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
          >
            <Box className='Modal-box'>
              <Typography id="modal-modal-title" variant="h6" component="h2" style={{ textAlign: 'center' }}>
                New experiment
              </Typography>
              <CreateForms
                className="design-component-instance-node-2"
                state="empty"
              />
              <ModalFooterItem
                actions="two"
                buttonButtonText="Cancel"
                buttonButtonText1="Create"
                buttonStateProp="disabled"
                cancel={false}
                className="design-component-instance-node-2"
                onClick={handleButtonClick}
              />
            </Box>
          </Modal>
        </div>
      </div>
    </div>
  );
}