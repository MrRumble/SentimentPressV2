import { useRef } from 'react';
import { Canvas, useFrame, useLoader } from '@react-three/fiber';
import { Sphere } from '@react-three/drei';
import * as THREE from 'three';
import earthTexture from './globeTexture.png'; // Ensure this path is correct

const Globe = ({ position = [0, 0, 0], scale = [2, 2, 2] }) => {
  const globeRef = useRef();
  const texture = useLoader(THREE.TextureLoader, earthTexture);

  useFrame(() => {
    if (globeRef.current) {
      globeRef.current.rotation.y += 0.002; // Adjust rotation speed if needed
    }
  });

  return (
    <Sphere ref={globeRef} args={[1, 32, 32]} position={position} scale={scale}>
      <meshStandardMaterial map={texture} />
    </Sphere>
  );
};

const GlobeComponent = ({ position, scale, lightSettings = {}, style = {}, canvasProps = {} }) => {
  // Default light settings
  const defaultLightSettings = {
    ambientLightIntensity: 0.5,
    directionalLightPosition: [5, 5, 5],
  };

  const { ambientLightIntensity, directionalLightPosition } = {
    ...defaultLightSettings,
    ...lightSettings,
  };

  return (
    <div style={{ width: '100%', height: '100%', ...style }}>
      <Canvas style={{ width: '100%', height: '100%' }} {...canvasProps}>
        <ambientLight intensity={ambientLightIntensity} />
        <directionalLight position={directionalLightPosition} />
        <Globe position={position} scale={scale} />
      </Canvas>
    </div>
  );
};

export default GlobeComponent;
