import { useEffect, useState } from "react";
import { Select, Spinner } from "../../../shared/components";
import { getAvailableModels, getCurrentModel } from "../services/modelService";

interface ModelSelectorProps {
  projectPath: string;
  onModelChange?: (model: string) => void;
}

export const ModelSelector: React.FC<ModelSelectorProps> = ({ projectPath, onModelChange }) => {
  const [models, setModels] = useState<string[]>([]);
  const [currentModel, setCurrentModel] = useState<string>("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      getAvailableModels(),
      getCurrentModel(projectPath)
    ]).then(([models, modelInfo]) => {
      setModels(models);
      setCurrentModel(modelInfo.embedding_model);
      setLoading(false);
    });
  }, [projectPath]);

  const handleChange = (model: string) => {
    setCurrentModel(model);
    if (onModelChange) onModelChange(model);
  };

  if (loading) return <Spinner />;

  return (
    <div>
      <label htmlFor="model-select">Embedding Model</label>
      <Select
        id="model-select"
        value={currentModel}
        options={models.map(m => ({ label: m, value: m }))}
        onChange={(e: React.ChangeEvent<HTMLSelectElement>) => handleChange(e.target.value)}
      />
    </div>
  );
};
