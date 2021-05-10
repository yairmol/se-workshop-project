import {
    Accordion,
    AccordionDetails,
    AccordionSummary,
    Card,
    Divider,
    Link,
    List,
    ListItem,
    Paper,
    Button, Tooltip
} from "@material-ui/core";
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";
import {useState} from "react";
import Grid from "@material-ui/core/Grid";

const useStyles = makeStyles((theme) => ({
    root: {
        width: '100%',
    },
    heading: {
        fontSize: theme.typography.pxToRem(20),
        flexBasis: '33.33%',
        flexShrink: 0,
    },
    secondaryHeading: {
        fontSize: theme.typography.pxToRem(15),
        color: theme.palette.text.secondary,
    },
    info: {
        fontSize: theme.typography.pxToRem(15),

    },
    accordion: {
        flexGrow: 1
    },
    paper: {
        padding: theme.spacing(3),
        display: 'flex',
        overflow: 'auto',
        flexDirection: 'column',
    },
    category: {
        padding: theme.spacing(1),
        display: 'flex',
        overflow: 'auto',
        flexDirection: 'column',
        textAlign: 'center',
        height: 40,
        width: 100
    },
    button: {
        padding: theme.spacing(1),
        display: 'flex',
        overflow: 'auto',
        flexDirection: 'column',
        width: 100,
    }
}));

export default function Product({product, remove_product_func, edit_product_func, permissions}) {
    const classes = useStyles();
    const [expanded, setExpanded] = useState(false);
    const onChange = () => {
        setExpanded(!expanded)
    }

    return (
        <Accordion expanded={expanded} onChange={onChange}>
            <AccordionSummary
                expandIcon={<ExpandMoreIcon/>}
            >
                <Grid container direction="column">
                    <Typography className={classes.heading}>{product.product_name}</Typography>
                    <Typography className={classes.secondaryHeading}>id: {product.product_id}</Typography>
                    <Typography className={classes.secondaryHeading}>price: ₪{product.price}</Typography>
                    <Typography className={classes.secondaryHeading}>quantity: {product.quantity}</Typography>
                </Grid>
            </AccordionSummary>
            <AccordionDetails>
                <Grid container direction="column">
                    <Grid item>
                            <Typography className={classes.secondaryHeading}>
                                {product.description}
                            </Typography>
                    </Grid>
                    <Grid item style={{padding:'10px', paddingTop:'25px', paddingBottom:'30px'}}>
                          <Grid container >
                              {product.categories.map((category) =>
                                  <Grid item xs={3}>
                                  <Paper className={classes.category}>{category}</Paper>
                                </Grid>
                              )}
                          </Grid>
                    </Grid>
                    {permissions.delete ?
                    <Grid item align="center" style={{padding:'5px'}}>
                          <Button onClick={() => {remove_product_func(product)}}
                                  size="small" className={classes.button} variant="contained" color="primary">
                              Remove
                          </Button>
                    </Grid>
                        :
                     <Grid item align="center" style={{padding:'5px'}}>
                         <Tooltip title="Remove product no permitted" placement="top-center">
                             <div style={{width:'50%'}}>
                                  <Button size="small" disabled className={classes.button} variant="contained" color="primary">
                                      Remove
                                  </Button>
                             </div>
                         </Tooltip>
                    </Grid>
                        }
                    {permissions.edit ?
                        <Grid item align="center" style={{padding: '5px'}}>
                            <Button onClick={() => {
                                edit_product_func(product)
                            }}
                                    size="small" className={classes.button} variant="contained" color="primary">
                                Edit
                            </Button>
                        </Grid>
                        :
                        <Grid item align="center" style={{padding: '5px'}}>
                            <Tooltip title="Edit product no permitted" placement="top-center">
                                <div style={{width: '50%'}}>
                                    <Button size="small" disabled className={classes.button} variant="contained"
                                            color="primary">
                                        Edit
                                    </Button>
                                </div>
                            </Tooltip>
                        </Grid>
                    }
                </Grid>
            </AccordionDetails>
        </Accordion>
    );
}