import "./Header.scss";
import { Link } from "@mui/material";
import { COPY } from "../../assets/copy/copy";

function Header() {
  return (
    <div className="header-wrapper">
      <div className="content">
        <div className="main-text">
          <div>Simulate My MRI Pulse</div>
        </div>
        <div className="spacer" />
        <div className="links">
          {COPY.HEADER.LINKS.map((link) => (
            <Link
              className="link"
              underline="hover"
              key={link.name}
              href={link.route}
            >
              {link.name}
            </Link>
          ))}
        </div>
        <div className="hori-line" />
      </div>
    </div>
  );
};

export default Header;
