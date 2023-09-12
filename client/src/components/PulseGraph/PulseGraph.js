import "./PulseGraph.scss";
import React from 'react';
import { Line } from "react-chartjs-2";
import Chart from "chart.js/auto";

const PulseGraph = (props) => {

    const data = {
        labels: JSON.parse(props.data.xdata),
        datasets: [
            {
                borderColor: '#61919F',
                fill: false,
                lineTension: 0,
                data: JSON.parse(props.data.ydata),
            },
        ],
    };

    return (
        <div classname="graph_area">
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
                        },
                        title: {
                            display: true,
                            text: 'Pulse Shape',
                            align: 'center',
                            color: '#222016'
                        }
                    },
                    scales: {
                        x: {
                          title: {
                            display: true,
                            text: 'Time (ms)'
                          },
                          ticks: {
                            stepSize: 0.20
                          }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Gamma-Bar B1 Amplitude'
                            }
                        }
                    },
                    elements: {
                        point:{
                            radius: 0
                        }
                    }
                }}
                />
            </div>
        </div>
    );
};

export default PulseGraph;
