import { useEffect, createRef } from "react";
import { createPluginUI } from "molstar/lib/mol-plugin-ui";
import { DefaultPluginUISpec } from 'molstar/lib/mol-plugin-ui/spec';
import "molstar/lib/mol-plugin-ui/skin/light.scss";


export function MolStarWrapper() {
  const parent = createRef();

  useEffect(() => {
    async function init() {
        window.molstar = await createPluginUI(parent.current,{
          ...DefaultPluginUISpec(),
          layout: {
              initial: {
                  isExpanded: false,
                  showControls: false
              }
          },
          components: {
              remoteState: 'none'
          }
      });

        const data = await window.molstar.builders.data.download(
          { url: "https://files.rcsb.org/download/3PTB.pdb" }, /* replace with your URL */
          { state: { isGhost: true } }
        );
        const trajectory =
          await window.molstar.builders.structure.parseTrajectory(data, "pdb");
        await window.molstar.builders.structure.hierarchy.applyPreset(
          trajectory,
          "default"
        );
    }
    init();
    return () => {
      window.molstar?.dispose();
      window.molstar = undefined;
    };
  }, []);
  return <div ref={parent} style={{ width: 640, height: 430 }}/>;
}