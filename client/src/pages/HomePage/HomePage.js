import "./HomePage.scss";
import { Link } from "react-router-dom";

function HomePage() {
    return (
      <div className="home">
        <h3>This is the Home Page!</h3>
        <p>click on the button to see the graphing:</p>
        <div className="button-wrapper">
          <Link to={"/simulation"} className="button">
            Graphing
          </Link>
        </div>
      </div>
    );
};

export default HomePage;
