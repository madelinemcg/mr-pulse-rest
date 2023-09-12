import "./SimGraph.scss";
import React from 'react';
import { Line } from "react-chartjs-2";
import Chart from "chart.js/auto";

const SimGraph = (props) => {

    const data = {
        labels: JSON.parse(props.data.xdata),
        datasets: [
            {
                label: 'Mxy',
                borderColor: '#61919F',
                fill: false,
                lineTension: 0,
                data: JSON.parse(props.data.mxy),
            },
            {
                label: 'Mz',
                borderColor: '#222016',
                fill: false,
                lineTension: 0,
                data: JSON.parse(props.data.mz),
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
                            position: 'top',
                        },
                        tooltip : {
                            enabled: false
                        },
                        title: {
                            display: true,
                            text: 'Simulation',
                            align: 'center',
                            color: '#222016'
                        }
                    },
                    scales: {
                        x: {
                          title: {
                            display: true,
                            text: 'Off Resonance (Hz)'
                          },
                          ticks: {
                            stepSize: 0.20
                          }
                        },
                        y: {
                            title: {
                                display: true,
                                text: '|Mxy|'
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

export default SimGraph;
