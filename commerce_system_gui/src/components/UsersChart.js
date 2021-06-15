import React, {PureComponent} from 'react';
import {LineChart, Line, XAxis, YAxis, Label, ResponsiveContainer, PieChart, Pie} from 'recharts';
import {
  Cell, Tooltip
} from 'recharts';


const colors = ["#ed553b", "#f6d55c", "#3caea3", "#20639b", "#7268a6", "#32a852"];


export default class UsersChart extends PureComponent {
  static jsfiddleUrl = 'https://jsfiddle.net/alidingling/30763kr7/';

  render() {
    return (
      <div>
        <PieChart width={300} height={300} margin={{
          top: 5, right: 30, left: 20, bottom: 5,
        }}>
          <Pie
            data={this.props.data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            fill="#8884d8"
            onClick={(x) => alert(x.name)}
            label
          >
            {
              this.props.data.map((entry, index) => <Cell fill={colors[index % colors.length]}/>)
            }
          </Pie>
          <Tooltip/>
        </PieChart>
      </div>
    );
  }
}


