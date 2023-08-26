import "./HomePage.scss";
import { Link } from "react-router-dom";

function HomePage() {
    return (
      <div className="home">
        <div className="button-wrapper">
          <Link to={"/simulation"} className="button">
            Graphing
          </Link>
        </div>
      </div>
    );
};

export default HomePage;
