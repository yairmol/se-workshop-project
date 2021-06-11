import React, {useState} from "react";
import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
} from "@material-ui/core";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";


export default function BuyProductPopup({product, add_to_cart_func}) {
  const [open, setOpen] = useState(true)

  const handleClose = () => {
    setOpen(false)
  }

  const done = () => {
    /*
    CALL FOR BUY
     */
    add_to_cart_func(product.product_id)
    handleClose()
  }

  return (
    <div>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          {product.product_name}
        </DialogTitle>
        <DialogContent>
          <Typography>{product.description}</Typography>
          <Typography>{product.quantity} available</Typography>
          <Typography>price is {product.price}ils</Typography>
          <Typography>{product.description}</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={done} color="primary">
            Add To Cart
          </Button>
          <Button onClick={handleClose} color="primary" autoFocus>
            Cancel
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
