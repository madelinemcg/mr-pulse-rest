import "./SimPage.scss";

function getPulse(cb) {
    fetch(`/graphql`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: `query {
          pulse {
            title
            type
            graph_fields
            sim_fields
            data_points
          }
        }`,
      }),
    })
      .then((res) => res.json())
      .then((res) => cb(res.data.pulse))
      .catch(console.error);
}

function changePulse(title, type, graph_fields, sim_fields, data_points, cb) {
    fetch(`/graphql`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: `mutation {
          changePulse(title: ${title}, type: ${JSON.stringify(type)},
           graph_fields: ${graph_fields}, sim_fields: ${sim_fields}, 
           data_points: ${data_points}) {
            title
            type
            graph_fields
            sim_fields
            data_points
          }
        }`,
      }),
    })
      .then((res) => res.json())
      .then((res) => cb(res.data))
      .catch(console.error);
}

function SimPage() {
    return (
        <div className="sim">
            <p>Graphing Here</p>
        </div>
    );
}

export default SimPage;
