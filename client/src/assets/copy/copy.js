export const COPY = {
    HEADER: {
        LINKS: [
          { name: "About", route: "https://simulate-my-mri-pulse.onrender.com" },
          { name: "Source Code", route: "https://github.com/madelinemcg/mr-pulse-rest" },
        ],
      },
    HOME: {
      BACKGROUND: ["Magnetic resonance imaging (MRI) scanners are controlled by writing pulse sequences, which manipulate the magnetic state of the sample or subject to generate images with the desired contrast characteristics.",
      "Radiofrequency (RF) pulses are used in these pulse sequences for excitation, refocusing, and providing spatial selectivity. The effect of an RF pulse can be simulated numerically using the Bloch equations, which is a first-order vector differential equation describing how magnetization responds to an RF input.",
      "Many different RF pulse types have been developed. RF pulses can be tailored to optimize performance for specific pulse sequences. Understanding how to optimize RF pulses is critical for those developing new MRI methods, as well as students learning basic MRI physics.",
      ],
    }
}
