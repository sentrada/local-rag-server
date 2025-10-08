import { useState } from "react";
import { ModelSelector } from "./ModelSelector";
import { ModelInfo } from "./ModelInfo";
import { ModelChangeModal } from "./ModelChangeModal";
import { useModelChange } from "../hooks/useModelChange";

// TODO: Replace with actual project path from store or props
const PROJECT_PATH = "/app/data/projects/AdvancedDatabaseExplorer";

export const SettingsPanel = () => {
	const [selectedModel, setSelectedModel] = useState<string>("");
	const [modalOpen, setModalOpen] = useState(false);
	const [pendingModel, setPendingModel] = useState<string>("");
	const { changeModel, loading, error, success } = useModelChange(PROJECT_PATH);

	const handleModelChange = (model: string) => {
		if (model !== selectedModel) {
			setPendingModel(model);
			setModalOpen(true);
		}
	};

	const handleConfirm = async () => {
		setModalOpen(false);
		await changeModel(pendingModel, true);
		setSelectedModel(pendingModel);
	};

	return (
		<div style={{ background: '#27272a', borderRadius: 8, padding: 20, marginTop: 32 }}>
			<h2 style={{ fontSize: 20, marginBottom: 12 }}>Beállítások (Settings)</h2>
			<div style={{ color: '#a1a1aa', marginBottom: 16 }}>
				<ModelSelector projectPath={PROJECT_PATH} onModelChange={handleModelChange} />
				<ModelInfo model={selectedModel} />
				{loading && <div style={{ marginTop: 12 }}><b>Indexelés folyamatban...</b> <span className="spinner" /></div>}
				{error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
				{success && <div style={{ color: 'green', marginTop: 8 }}>Sikeres modellváltás és újraindexelés!</div>}
			</div>
			<ModelChangeModal
				open={modalOpen}
				onConfirm={handleConfirm}
				onCancel={() => setModalOpen(false)}
				newModel={pendingModel}
			/>
		</div>
	);
};
