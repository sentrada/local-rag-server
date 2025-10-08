import React from "react";
import { Modal, Button } from "../../../shared/components";

interface ModelChangeModalProps {
  open: boolean;
  onConfirm: () => void;
  onCancel: () => void;
  newModel: string;
}

export const ModelChangeModal: React.FC<ModelChangeModalProps> = ({ open, onConfirm, onCancel, newModel }) => (
  <Modal open={open} onClose={onCancel}>
    <h3>Modell váltás megerősítése</h3>
    <p>
      A(z) <b>{newModel}</b> modell kiválasztása törli a jelenlegi indexet, és újraindexelést igényel.<br />
      <span style={{ color: 'orange' }}>Ez a művelet időigényes lehet, és a nagyobb modellek lassabbak!</span>
    </p>
    <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
      <Button onClick={onConfirm} color="danger">Folytatom, törlés és újraindex</Button>
      <Button onClick={onCancel} color="secondary">Mégsem</Button>
    </div>
  </Modal>
);
