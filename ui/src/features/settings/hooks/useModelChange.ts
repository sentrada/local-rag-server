import { useState } from "react";
import { setProjectModel } from "../services/modelService";

export function useModelChange(projectPath: string) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const changeModel = async (model: string, autoReindex = false) => {
    setLoading(true);
    setError(null);
    setSuccess(false);
    try {
      await setProjectModel(projectPath, model, autoReindex);
      setSuccess(true);
    } catch (e: any) {
      setError(e?.message || "Hiba történt a modell váltáskor");
    } finally {
      setLoading(false);
    }
  };

  return { changeModel, loading, error, success };
}
