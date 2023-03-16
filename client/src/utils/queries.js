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
      .then(res => res.json())
      .then(res => cb(res.data.getPulse))
      .catch(console.error)
  }
