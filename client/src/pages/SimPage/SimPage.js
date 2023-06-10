import "./SimPage.scss";
import PulseGraph from '../../components/PulseGraph/PulseGraph';
import { useState, useEffect } from "react";
import Form from 'react-bootstrap/Form';

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
    fetch('/pulsechange', {
        method:"POST",
        cache:"no-cache",
        headers:{
            "Content_Type":"application/json",
            "Accept":"application/json",
        },
        body:JSON.stringify({
            type: event.target.value
        })
    })
    .then(res => res.json())
    .then(data => {
        setCurrentPulse(({
        type: data.type,
        graph_data: {
            'xdata': data.graph_data.xdata,
            'ydata': data.graph_data.ydata,
        },
        graph_params: data.graph_params
        }));
    });
    }

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
                    <div>{JSON.parse(currentPulse.graph_params).map((param) => {
                        <div key={param.name}>
                            <div>{param.name}</div>
                            <div>{param.val}</div>
                        </div>
                        
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
