import "./PulseGraph.scss";
import React from 'react';
import { Line } from "react-chartjs-2";
import Chart from "chart.js/auto";

const data = {
    labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    datasets: [
        {
            label: "hi",
            borderColor: "rgb(255, 99, 132)",
            fill: false,
            lineTension: 0.5,
            data: [1, 2, 3, 4, 5, 6, 4, 2, 4, 6],
        },
    ],
};

const PulseGraph = () => {
    return (
        <div classname="graph_area">
            <p className="title">Title Goes Here</p>
            <div className="graph">
                <Line
                data={data} 
                options={{
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }}
                />
            </div>
        </div>
    );
};

export default PulseGraph;
