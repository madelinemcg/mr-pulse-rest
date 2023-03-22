import { Routes as BRoutes, Navigate, Route } from "react-router-dom";
import { useMemo } from "react";
import HomePage from "../pages/HomePage/HomePage";
import SimPage from "../pages/SimPage/SimPage";

export const ROUTES = {
  HOME: "/",
  SIM: "/simulation",
};

export const Pages = () => {
  const redirect = useMemo(() => {
    return <Navigate replace={true} to={ROUTES.HOME} />;
  }, []);

  return (
    <BRoutes>
      <Route path={ROUTES.HOME} element={<HomePage />} />
      <Route path={ROUTES.SIM} element={<SimPage />} />
      <Route path="*" element={redirect} />
    </BRoutes>
  );
};
