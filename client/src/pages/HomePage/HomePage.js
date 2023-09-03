import "./HomePage.scss";
import { Link } from "react-router-dom";
import { COPY } from "../../assets/copy/copy";
import MRIImage from "../../assets/images/MRIImage.png";
import PulseImage from "../../assets/images/PulseImage.png"

function HomePage() {
    return (
      <div className="home">
        <div className="img">
          <div className="img-background">
            <img className="main-img" src={MRIImage} alt="" />
          </div>
        </div>
        <div className="line" />
        <div className="about-textbox">
          <div className="title">About The Project</div>
          <div className="background">
            {COPY.HOME.BACKGROUND.map((paragraph) => (
              <div className="paragraph" key={paragraph} >
                {paragraph}
              </div>
            ))}
          </div>
          <img className="chart-img" src={PulseImage} alt="" />
          <div className="button-wrapper">
            <Link to={"/simulation"} className="button">
              Simulate Pulse
            </Link>
          </div>
        </div>
        <div className="footer"></div>
      </div>
    );
};

export default HomePage;
