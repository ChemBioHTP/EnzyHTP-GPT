import React, { useEffect, createRef } from "react";
import { createPluginUI } from "molstar/lib/mol-plugin-ui";
import { DefaultPluginUISpec } from 'molstar/lib/mol-plugin-ui/spec';
import "molstar/lib/mol-plugin-ui/skin/light.scss";

import { Script } from 'molstar/lib/mol-script/script';
import { StructureSelection } from 'molstar/lib/mol-model/structure/query';
import { ColorNames } from 'molstar/lib/mol-util/color/names';
import { PluginCommands } from 'molstar/lib/mol-plugin/commands';
// import { Structure } from '../mol-model/structure';
import { MolScriptBuilder as MS, MolScriptBuilder } from 'molstar/lib/mol-script/language/builder';
import { Expression } from 'molstar/lib/mol-script/language/expression';
import {  StructureSelectionQuery } from 'molstar/lib/mol-plugin-state/helpers/structure-selection-query'

export function MolStarWrapper() {
  const parent = createRef();
  useEffect(() => {
    async function init() {
      // Create the plugin UI for Mol* viewer
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

      // Load the structure
      const data = await window.molstar.builders.data.download(
        { url: "https://files.rcsb.org/download/3PTB.pdb" }, /* replace with your URL */
        { state: { isGhost: true } }
      );
      const trajectory =
        await window.molstar.builders.structure.parseTrajectory(data, "pdb");
      const structure = await window.molstar.builders.structure.hierarchy.applyPreset(
        trajectory,
        "default"
      );

      // const renderer = window.molstar.canvas3d.props.renderer;
      // PluginCommands.Canvas3D.SetSettings(window.molstar, { settings: { renderer: { ...renderer, backgroundColor: ColorNames.red /* or: 0xff0000 as Color */ } } });
      
      const structure_data = window.molstar.managers.structure.hierarchy.current.structures[0]?.cell.obj?.data;
      if (!structure_data) return;

      // const selection = Script.getStructureSelection(Q => Q.struct.generator.atomGroups({
      //     'chain-test': Q.core.rel.eq(['B', Q.ammp('label_asym_id')])
      // }), structure_data);

      // const ligandData = window.molstar.managers.structure.hierarchy.selection.structures[0]?.components[0]?.cell.obj?.data;

      const args = [['A', 10, 15], ['A', 20, 25]]
      const groups = [];
      for (var chain of args) {
        groups.push(MS.struct.generator.atomGroups({
          // "chain-test": MS.core.rel.eq([MolScriptBuilder.struct.atomProperty.macromolecular.auth_asym_id(), chain[0]]),
          "residue-test": MS.core.rel.inRange([MolScriptBuilder.struct.atomProperty.macromolecular.label_seq_id(), chain[1], chain[2]])
        }));
      }

      var sq = StructureSelectionQuery('residue_range_10_15_in_A', MS.struct.combinator.merge(groups));
      
      console.log(sq);
  
      // var selection = await window.molstar.managers.structure.selection.fromSelectionQuery('set', sq);

      var selection = Script.getStructureSelection(MS => MS.struct.generator.atomGroups({
        'chain-test'  : MS.core.rel.eq([MS.struct.atomProperty.macromolecular.auth_asym_id(), "A"]),
        "residue-test": MS.core.rel.eq([MS.struct.atomProperty.macromolecular.label_seq_id(), 24]),
      }), structure_data);

      console.log(selection);
      // const selection = await select_multiple(window.molstar);

      const loci = StructureSelection.toLociWithSourceUnits(selection);
      // window.molstar.managers.interactivity.lociHighlights.highlightOnly({ loci }); // loci: Loci
      // window.molstar.managers.camera.focusLoci(loci);
      const renderer = window.molstar.canvas3d.props.renderer;
      PluginCommands.Canvas3D.SetSettings(window.molstar, { settings: { renderer: { ...renderer, selectColor: ColorNames.red /* or: 0xff0000 as Color */ } } });

      
    }
    init();
    return () => {
      window.molstar?.dispose();
      window.molstar = undefined;
    };
  }, []);

  return <div ref={parent} style={{ width: 640, height: 430 }} />;
}

export default MolStarWrapper;
