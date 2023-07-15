import "./SimPage.scss";
import PulseGraph from '../../components/PulseGraph/PulseGraph';
import { useState, useEffect } from "react";
import Form from 'react-bootstrap/Form';
import Slider from '@mui/material/Slider';

function SimPage() {
    const [currentPulse, setCurrentPulse] = useState({
        'type': 'Choose Pulse',
        'graph_data': {
            'xdata': '[]',
            'ydata': '[]',
        },
        'graph_params': '[]'
    });
    
    // When page is loaded, get default data from backend
    useEffect(() => {
    fetch('/pulse').then(res => res.json()).then(data => {
        setCurrentPulse(({
        type: data.type,
        graph_data: {
            'xdata': data.graph_data.xdata,
            'ydata': data.graph_data.ydata,
        },
        graph_params: data.graph_params
        }));
    });
    }, []);

    // Sends new pulse type to api to recalculate values
    let handleTypeChange = (event) => {
    console.log("Graph_params: ", currentPulse.graph_params)
    fetch('/pulsechange', {
        method:"POST",
        cache:"no-cache",
        headers:{
            "Content_Type":"application/json",
            "Accept":"application/json",
        },
        body:JSON.stringify({
            type: event.target.value,
            graph_params: currentPulse.graph_params
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Graph_params from json: ", data.graph_params);
        setCurrentPulse(({
        type: data.type,
        graph_data: {
            'xdata': data.graph_data.xdata,
            'ydata': data.graph_data.ydata,
        },
        graph_params: data.graph_params
        }));
    })
    .then(console.log("Graph_params: ", currentPulse.graph_params)
    )}

    // Updates graph values based on new parameters
    // let handleGraphParamChange = (event) => {
    //     console.log(event);
        // Replace changed param in graph_params
        // currentPulse.graph_params.name[event.name]
        // setCurrentPulse(({
        //     ...currentPulse,
        //     graph_params: 
        // }));
        // Fetch new data
        // fetch('/pulsegraphparamchange', {
        //     method:"POST",
        //     cache:"no-cache",
        //     headers:{
        //         "Content_Type":"application/json",
        //         "Accept":"application/json",
        //     },
        //     body:JSON.stringify({
        //         type: currentPulse.type,
        //         graph_params: currentPulse.graph_params
        //     })
        // })
        // .then(res => res.json())
        // .then(data => {
        //     setCurrentPulse(({
        //     ...currentPulse,
        //     type: data.type,
        //     graph_data: {
        //         'xdata': data.graph_data.xdata,
        //         'ydata': data.graph_data.ydata,
        //     }
        //     }));
        // })
    // }

    return (
        <div className="sim">
            <p>Graphing Page</p>
            <p>Current pulse type is {currentPulse.type}</p>
            <div className="options">
                <div className="choices">
                    <div className="pulse_choice">
                        <Form.Select onChange={handleTypeChange}>
                            <option value="none">Choose Pulse</option>
                            <option value="sinc">Sinc</option>
                            <option value="gauss">Guassian</option>
                        </Form.Select>
                    </div>
                    <div>{JSON.parse(currentPulse.graph_params).map((param, index) => {
                        return (
                            <div key={`${param}`}>
                                <div>{param.name}</div>
                                <div>
                                    <Slider
                                        defaultValue={param.val}
                                        step={param.step}
                                        min={param.min}
                                        max={param.max}
                                        valueLabelDisplay="auto"
                                    />
                                </div>
                            </div>
                        )
                    })}</div>
                </div>
                <div className="graph">
                    <PulseGraph data={currentPulse.graph_data} />
                </div>
            </div>
        </div>
    );
}

export default SimPage;
