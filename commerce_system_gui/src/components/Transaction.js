import {
    Accordion,
    AccordionDetails,
    AccordionSummary,
    Card,
    Divider,
    Link,
    List,
    ListItem,
    Paper
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
    }
}));

function ProductView({product}) {
    const classes = useStyles();

    return (
        <Paper className={classes.paper}>
            <Grid container spacing={5} direction="row" alignItems="center">
                <Grid item>
                    <Typography className={classes.secondaryHeading}>name: {product.product_name}</Typography>
                </Grid>
                <Grid item>
                    <Typography className={classes.secondaryHeading}>price: {product.price}</Typography>
                </Grid>
                <Grid item>
                    <Typography className={classes.secondaryHeading}>amount {product.amount}</Typography>
                </Grid>
            </Grid>
        </Paper>
    )
}

export function Transaction({transaction}) {
    const classes = useStyles();
    const [expanded, setExpanded] = useState(false);
    const onChange = () => {
        setExpanded(!expanded)
    }
    const date = new Date(transaction.date * 1000)

    return (
        <Accordion expanded={expanded} onChange={onChange}>
            <AccordionSummary
                expandIcon={<ExpandMoreIcon/>}
                aria-controls={`panel${transaction.id}bh-content`}
                id={`panel${transaction.id}bh-header`}
            >
                <Grid container direction="column">
                    <Link className={classes.heading}>Transaction ID: {transaction.id}</Link>
                    <Typography className={classes.secondaryHeading}>bought from shop: {transaction.shop.shop_name}</Typography>
                    <Typography className={classes.secondaryHeading}>total: {transaction.price}</Typography>
                    <Typography className={classes.secondaryHeading}>date: {date.toString()}</Typography>
                </Grid>
            </AccordionSummary>
            <AccordionDetails>
                <Grid container direction="column">
                    <Grid item>
                        <Typography>Products</Typography>
                    </Grid>
                    <Grid item>
                        <List>
                            {transaction.products.map((product, index) =>
                                <ListItem item key={product.product_id}><ProductView product={product}/></ListItem>)}
                        </List>
                    </Grid>
                </Grid>
            </AccordionDetails>
        </Accordion>
    );
}