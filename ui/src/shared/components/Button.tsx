import React from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  color?: "primary" | "secondary" | "danger";
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({ color = "primary", children, ...props }) => {
  const colors = {
    primary: "#3b82f6",
    secondary: "#6b7280",
    danger: "#ef4444",
  };

  return (
    <button
      {...props}
      style={{
        backgroundColor: colors[color],
        color: "white",
        padding: "8px 16px",
        borderRadius: 4,
        border: "none",
        cursor: "pointer",
        fontSize: 14,
        fontWeight: 500,
        ...props.style,
      }}
    >
      {children}
    </button>
  );
};
