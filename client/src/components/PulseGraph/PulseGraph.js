import "./PulseGraph.scss";
import React from 'react';
import { Line } from "react-chartjs-2";
import Chart from "chart.js/auto";

const PulseGraph = (props) => {
    const data = {
        labels: JSON.parse(props.data.xdata),
        datasets: [
            {
                borderColor: "rgb(255, 99, 132)",
                fill: false,
                lineTension: 0.5,
                data: JSON.parse(props.data.ydata),
            },
        ],
    };

    return (
        <div classname="graph_area">
            <p className="title">Title Goes Here</p>
            <div className="graph">
                <Line
                className="canvas"
                data={data} 
                options={{
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip : {
                            enabled: false
                        }
                    }
                }}
                />
            </div>
        </div>
    );
};

export default PulseGraph;
