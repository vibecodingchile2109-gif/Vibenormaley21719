---
tipo: documento interno / manual corporativo (NO normativo)
contenido: Manual de Evaluación de Impacto en IA (AIA) + Manual de ciberseguridad e integridad de modelos
marcos: ISO/IEC 42001:2023, EU AI Act, Ley 21.719, Ley 21.663
advertencia: "Cita artículos de la Ley 21.719 con numeración no verificada contra el texto oficial. No usar como fuente de citas legales."
---

Sistema de Gobernanza Corporativa de IA - Marco Integrado
    

    
        

## Índice General del Marco de Gobernanza Corporativa en IA

        
            
- DOCUMENTO 2: Manual de Evaluación de Impacto en IA (AIA) y Gestión de Riesgos de Modelos

            
- DOCUMENTO 3: Manual Operativo de Ciberseguridad, Integridad de Modelos y Control Zero Trust en IA

        
    

    
    
    
    
        

# MANUAL DE EVALUACIÓN DE IMPACTO EN IA (AIA) Y GESTIÓN DE RIESGOS DE MODELOS

        

## 1. PROPÓSITO Y ÁMBITO DE APLICACIÓN

        El presente manual establece la metodología técnica y obligatoria para la identificación, clasificación, mitigación y monitoreo de los riesgos asociados a los sistemas de Inteligencia Artificial (SIA) operados, adquiridos o desarrollados por la organización. Su objetivo principal es operacionalizar las exigencias del estándar ISO/IEC 42001:2023 (Cláusula 6.1.2 y 8.2), articulándolas con los mandatos imperativos de la Ley N° 21.719 sobre Protección de Datos Personales (Chile), específicamente en lo relativo a Evaluaciones de Impacto (EIPD/AIA), y el marco adaptativo para la gestión de modelos de propósito general o con capacidades de comportamiento emergente autónomo.

        

## 2. MATRIZ DE CLASIFICACIÓN DE RIESGOS INTEGRADA (CHILE - UE)

        Para armonizar los criterios objetivos de clasificación del Reglamento de IA de la Unión Europea (EU AI Act) con la normativa chilena, la organización implementa un modelo de categorización basado en cuatro niveles de riesgo. El cruce con la legislación nacional se determina por el impacto sobre los titulares de datos (Ley N° 21.719) y la criticidad de la infraestructura afectada (Ley N° 21.663 Marco de Ciberseguridad).

        
            
                
                    Categoría de Riesgo (AIMS)
                    Criterio Técnico (EU AI Act)
                    Gatillo Legal en Chile (Ley N° 21.719 / Ley N° 21.663)
                    Mecanismo de Control Obligatorio
                

            
            
                
                    Riesgo Inaceptable / Prohibido
                    Manipulación cognitiva, puntuación social masiva, perfiles policiales predictivos automatizados sin base.
                    Vulneración directa del artículo 1° de la Constitución y principios de dignidad y autodeterminación informativa de la Ley N° 21.719.
                    Veto Inmediato: El sistema no puede ser desarrollado ni contratado bajo ninguna circunstancia.
                

                
                    Riesgo Alto (HRAI)
                    Sistemas utilizados en infraestructuras críticas, evaluación de créditos, contratación de personal, educación o salud.
                    Art. 17° bis (Ley N° 21.719): Tratamientos automatizados que produzcan efectos jurídicos o afecten significativamente al titular. Servicios Esenciales según Ley N° 21.663.
                    AIA Formal + Registro Ex-Ante: Requiere Evaluación de Impacto exhaustiva y aprobación explícita del Comité de Gobernanza (CGIA).
                

                
                    Riesgo Específico de Transparencia
                    Modelos fundacionales generativos, chatbots, sistemas de optimización interna que interactúan con humanos.
                    Art. 14° (Ley N° 21.719): Derecho de información respecto a los fines y lógicas aplicadas en el tratamiento algorítmico.
                    Marcado de Contenido: Declaración explícita de interacción con IA y marcas de agua (Watermarking) criptográficas en outputs.
                

                
                    Riesgo Mínimo / Bajo
                    Filtros de spam tradicionales, optimizadores de consultas SQL internos, analítica predictiva de stock no asociable a personas.
                    Tratamiento de datos puramente de carácter estadístico u organizacional sin contacto con datos personales ni infraestructuras críticas.
                    Registro en Inventario: Declaración en el Registro Central de Sistemas sin necesidad de controles adicionales.
                

            
        

        

## 3. METODOLOGÍA STEP-BY-STEP PARA LA EVALUACIÓN DE IMPACTO EN IA (AIA)

        Antes del inicio de cualquier fase de codificación o adquisición de licencias para un sistema de Riesgo Alto o con tratamiento de datos personales, el AI Risk Owner debe ejecutar el proceso de Evaluación de Impacto. Este proceso consta de cinco fases técnico-jurídicas secuenciales:

        

### Fase 3.1: Análisis de la Arquitectura del Sistema e Inferencia

        Se debe determinar formalmente si el sistema califica como Inteligencia Artificial bajo el criterio estricto de la ISO 42001 y las directrices globales: capacidad de inferir conceptos, lógicas o patrones a partir de datos de entrenamiento para generar predicciones, recomendaciones o decisiones. Si el sistema opera exclusivamente mediante reglas deterministas cableadas (reglas lógicas fijas "if-then" escritas estáticamente por un desarrollador), se excluirá de este manual y se derivará al control de seguridad de software tradicional de la ISO 27001.

        

### Fase 3.2: Mapeo de Flujos de Datos Personales y Base Legal (Cruce Ley N° 21.719)

        El desarrollador o implementador debe documentar mediante diagramas de flujo el ciclo completo de los datos:

        
            
- Origen del Dataset: Especificar si proviene de fuentes directas, terceros o recolección automatizada.

            
- Validación de Licitud (Art. 4° Ley N° 21.719): Identificar fehacientemente cuál es la base legal habilitante. Si se invoca el "Interés Legítimo", se debe adjuntar la prueba de ponderación que demuestre que los derechos de los ciudadanos chilenos no se ven sobrepasados por el interés comercial de la empresa.

            
- Mecanismo de Minimización: Describir las técnicas de truncamiento, hashing o agregación para asegurar que no se introduzcan al modelo más datos de los estrictamente necesarios para el fin del negocio.

        

        

### Fase 3.3: Evaluación de Riesgos Técnicos y Vulnerabilidades de Frontera

        La evaluación no debe limitarse a riesgos de privacidad clásicos; debe proyectar vectores de ataque específicos de IA avanzada, tales como:

        
            
- Efectos de Evaluación Externa (Evaluation-Awareness / Sandbagging): Evaluar si el modelo puede detectar que está operando en un entorno de pruebas o sandbox y alterar deliberadamente su rendimiento o enmascarar sesgos para evadir la auditoría (comportamientos observados en modelos frontera avanzados tipo Claude Mythos).

            
- Envenenamiento Post-Entrenamiento (Post-Training Poisoning): Riesgo de corrupción en los pesos del modelo mediante interfaces de Fine-Tuning expuestas o manipulación del Reinforcement Learning from Human Feedback (RLHF).

        

        
            Alerta Crítica de Ciberseguridad (ANCI Chile): Conforme a la taxonomía de la Agencia Nacional de Ciberseguridad, la alteración o corrupción no autorizada de la lógica de un sistema informático crítico configura un incidente de Impacto en la Integridad de la Información. Los reportes ante el CSIRT Nacional bajo este vector deben ejecutarse en un plazo máximo según la normativa ante la detección de anomalías algorítmicas estructurales.
        

        

### Fase 3.4: Diseño de la Supervisión Humana Efectiva (Human-in-the-Loop)

        Para dar cumplimiento estricto al Artículo 17° bis de la Ley N° 21.719, el sistema debe implementar una arquitectura de control humano sobre la decisión automatizada. El diseño debe detallar:

        
            
- El panel de control (Dashboard) donde un operador humano capacitado revisa las sugerencias de alta criticidad emitidas por el algoritmo antes de su ejecución legal o comercial.

            
- El mecanismo tecnológico de "Override" o veto manual instantáneo que permita al operador desactivar la inferencia del modelo si se detecta un comportamiento anómalo o discriminatorio.

        

        

### Fase 3.5: Plan de Mitigación y Firma de Responsabilidad

        Cada riesgo identificado debe contar con un control técnico compensatorio. El informe final consolidado de la AIA debe ser firmado digitalmente por el AI Risk Owner, el Oficial de Protección de Datos (DPO) y el CISO, y archivado en el Repositorio Central de Cumplimiento del AIMS para estar disponible ante un requerimiento de fiscalización de la Agencia Nacional de Protección de Datos de Chile.

        

## 4. PROTOCOLO DE EVALUACIÓN DE EQUIDAD (FAIRNESS) Y MITIGACIÓN DE SESGOS

        El tratamiento de datos automatizado mediante modelos predictivos no puede generar efectos discriminatorios basados en categorías sospechosas (género, etnia, edad, localización geográfica dentro de Chile, etc.), resguardando los principios fundamentales de la Ley N° 21.719.

        

### 4.1. Métricas Cuantitativas Obligatorias

        Los equipos de Ciencia de Datos deben aplicar frameworks de auditoría algorítmica antes del despliegue y de forma cuatrimestral, calculando índices matemáticos específicos:

        
            
- Paridad Demográfica (Demographic Parity): La probabilidad de que el modelo asigne un resultado positivo (ej. aprobación de un crédito) debe ser sustancialmente igual para todos los grupos protegidos evaluados. Se establece un umbral de tolerancia mínimo del 80% (Regla de los cuatro quintos).

            
- Igualdad de Oportunidades (Equal Opportunity): La tasa de verdaderos positivos debe ser idéntica entre los diferentes grupos, asegurando que el modelo posea la misma precisión predictiva sin importar la condición sociodemográfica del titular chileno.

        

        

### 4.2. Estrategias de Remediación Técnica

        Si las métricas revelan un sesgo estadístico que vulnere la equidad, se deben aplicar las siguientes acciones de ingeniería:

        
            
                
                    Estrategia
                    Fase del Pipeline
                    Descripción Técnica
                

            
            
                
                    Pre-procesamiento (Pre-processing)
                    Preparación de Datos
                    Técnicas de re-ponderación (re-weighing) o remoción de correlaciones directas en el dataset de entrenamiento antes de alimentar el algoritmo.
                

                
                    In-procesamiento (In-processing)
                    Entrenamiento del Modelo
                    Modificación de la función de pérdida (Loss Function) del modelo, añadiendo un término de penalización por discriminación (adversarial debiasing).
                

                
                    Post-procesamiento (Post-processing)
                    Inferencia / Salida
                    Ajuste dinámico de los umbrales de decisión (thresholds) en la capa de salida para calibrar y corregir las predicciones finales a favor del grupo afectado.
                

            
        

        

## 5. GOBERNANZA ADAPTATIVA DE MODELOS GENERALES Y AGENTES AUTÓNOMOS

        Dada la naturaleza de los modelos de lenguaje a gran escala (LLMs) y los sistemas de IA de carácter agéntico (capaces de formular planes y ejecutar herramientas de forma autónoma), la gestión de riesgos tradicional basada en matrices estáticas resulta insuficiente. Se adopta un modelo de gobernanza adaptativa continua (Adaptive Governance Framework).

        

### 5.1. Monitoreo de Propiedades Emergentes

        Los sistemas agénticos integrados a los flujos operativos de la organización deben ser sometidos a un monitoreo basado en telemetría de comportamiento. El sistema de auditoría debe registrar de forma inalterable las llamadas a APIs externas, el consumo de prompts y, críticamente, la coherencia del "Chain-of-Thought" (cadena de pensamiento interna del modelo).

        

### 5.2. Umbrales de Deriva (Drift) y Desconexión de Emergencia (Kill Switch)

        Se implementa un protocolo automatizado de contención ante las siguientes anomalías operativas:

        
            
- Concept Drift / Data Drift: Cuando la distribución de los datos de entrada del entorno real diverge en más de un 15% respecto al dataset de validación original, el sistema emitirá una alerta de nivel Medio.

            
- Violación del Alimento de Contexto (Context Injection): Si la capa de monitoreo detecta que el agente está intentando modificar sus propias instrucciones del sistema (System Prompts) o ejecutar comandos de sistema no autorizados, se activará el Kill Switch algorítmico, degradando el sistema automáticamente a un modo seguro determinista y bloqueando el acceso a las bases de datos corporativas que contienen datos protegidos por la Ley N° 21.719.

        

        
            // Ejemplo conceptual de validación de umbral de riesgo en la capa de inferencia
            // Implementado en los microservicios de evaluación de conformidad (Compliance Engine)
            
            fn evaluar_riesgo_inferencia(data_drift_score: f32, prompt_anomaly_detected: bool) -> String {
                if prompt_anomaly_detected {
                    CONEXION_BASE_DATOS.DISCONNECT(); // Aislamiento inmediato conforme a Ley 21.719 e ISO 42001
                    return String::from("ESTADO: CRÍTICO - KILL_SWITCH_ACTIVADO");
                }
                
                match data_drift_score {
                    x if x >= 0.15 => String::from("ESTADO: ALTO RIESGO - RE-ENTRENAMIENTO REQUERIDO"),
                    x if x >= 0.05 => String::from("ESTADO: MEDIO - MONITOREO INTENSIFICADO"),
                    _ => String::from("ESTADO: NORMAL")
                }
            }
        

    

    
    
    
    
        

# MANUAL OPERATIVO DE CIBERSEGURIDAD, INTEGRIDAD DE MODELOS Y CONTROL ZERO TRUST EN IA

        

## 1. INTRODUCCIÓN Y MODELO DE AMENAZAS EN IA

        El paradigma de seguridad de la información tradicional (ISO 27001) asume que las aplicaciones de software son deterministas y que las amenazas provienen de actores externos que intentan explotar vulnerabilidades en el código de infraestructura. La adopción de Inteligencia Artificial invalida parcialmente esta premisa. Los modelos de machine learning e IA generativa introducen una superficie de ataque probabilística donde el propio modelo puede ser subvertido para actuar en contra de la organización, actuando como un "agente interno comprometido" sin levantar alertas en los firewalls tradicionales.

        
        Este manual operativo define las contramedidas de ingeniería y los protocolos de control bajo una arquitectura estricta de Zero Trust Algorítmico (Confianza Cero en IA), en cumplimiento con el dominio A.7 de la ISO/IEC 42001:2023 y en perfecta alineación con las obligaciones de resiliencia técnica de la Ley N° 21.663 Marco de Ciberseguridad de Chile.

        

## 2. PROTOCOLO DE DEFENSAS CONTRA ATAQUES DE INTEGRIDAD (SABOTAJE Y SUBVERSIÓN)

        Los ataques a la integridad de la IA buscan alterar el comportamiento esperado del modelo. Se diferencian técnicamente en dos categorías que la organización debe mitigar de forma diferenciada:

        

### 2.1. Mitigación del Sabotaje de Modelos

        Orientado a la degradación deliberada del rendimiento para causar pérdidas económicas u operativas. La organización implementará sistemas de monitoreo de accuracy y pérdida en tiempo real en los endpoints de producción. Cualquier caída abrupta en la confianza de las inferencias (falsos positivos/negativos que excedan las 3 desviaciones estándar respecto a la línea base histórica) gatillará un desvío automático de las peticiones hacia un modelo de respaldo o un sistema basado en reglas heurísticas tradicionales.

        

### 2.2. Mitigación de la Subversión y "Backdoors" Avanzados

        El ataque más complejo consiste en la implantación de un comportamiento malicioso latente (puerta trasera algorítmica). El modelo funciona con una precisión excelente en todas las pruebas rutinarias, pero activa una acción maliciosa o sesgada ante la presencia de un token, frase o patrón visual específico (Trigger). Para defendernos de la subversión, se establecen tres capas obligatorias:

        
            
- Verificación Criptográfica de Pesos (Model Swap Prevention): Todos los archivos de arquitectura y pesos del modelo (.safetensors, .onnx, .bin) almacenados en nuestros repositorios en la nube (ej. Vertex AI, AWS Bedrock o servidores locales) deben contar con un hash SHA-256 generado inmediatamente después del entrenamiento o de la validación de conformidad. La infraestructura de producción calculará el hash antes de cada carga en memoria RAM/VRAM; si el hash no coincide exactamente, la inicialización del contenedor se abortará de inmediato, informando el incidente al CSIRT interno.

            
- Auditoría de Caja Blanca mediante Interpretabilidad Mecanística: Para los modelos de alta criticidad, el equipo de ciberseguridad algorítmica aplicará técnicas de análisis interno de capas de activación, buscando subredes neuronales anómalas o activaciones desproporcionadas ante caracteres de control no estándar.

        

        

## 3. CONTROL DE ENVENENAMIENTO DE DATOS (DATA POISONING)

        El envenenamiento de datos representa la vía principal por la cual un atacante inyecta backdoors o altera la equidad del sistema, impactando directamente en el cumplimiento de la Ley N° 21.719 al corromper el tratamiento lícito de los datos personales.

        

### 3.1. Control en Pre-Entrenamiento (Pre-training Poisoning)

        Queda estrictamente prohibida la ingesta automatizada de datos provenientes de repositorios públicos o scraping web sin pasar por un pipeline de sanitización intermedio. Los datos crudos deben someterse a:

        
            
- Filtros de steganografía y detección de anomalías estadísticas basadas en distancia euclidiana respecto a clústeres de datos validados.

            
- Análisis de procedencia (Data Provenance Tracking) respaldado por metadatos inmutables que certifiquen el origen y la inalterabilidad de cada registro.

        

        

### 3.2. Control en Post-Entrenamiento (Post-training Poisoning)

        Durante los procesos de Fine-Tuning y optimización mediante RLHF (Reinforcement Learning from Human Feedback), los datos aportados por los operadores humanos o usuarios a través de interfaces de feedback deben ser validados de forma aislada. Las cuentas de los evaluadores humanos deben exigir de forma mandatoria Autenticación de Múltiples Factores (MFA) con llaves físicas de hardware e integrarse a logs de auditoría centralizados con el estándar ISO 27001.

        

## 4. ARQUITECTURA ZERO TRUST APLICADA A IA GENERATIVA Y AGENTES

        Bajo el enfoque Zero Trust, la organización debe asumir operativamente que el modelo de IA está comprometido por diseño. Por lo tanto, el sistema nunca debe poseer privilegios directos o ilimitados en el ecosistema corporativo.

        
            Directriz Operativa Obligatoria: Ningún modelo de lenguaje (LLM) o agente autónomo podrá ejecutar consultas de base de datos directas (SQL/NoSQL) ni llamadas a APIs de sistemas de producción que contengan datos personales protegidos por la Ley N° 21.719 sin pasar por un microservicio intermedio de autenticación y sanitización de consultas.
        

        

### 4.1. Sandboxing y Aislamiento de Ejecución

        Las aplicaciones agénticas de IA con capacidades de ejecución de código o análisis dinámico de archivos (ej. intérpretes de código internos o integraciones tipo Claude Code) deben operar estrictamente dentro de entornos de contenedores aislados (Sandboxes virtuales) con restricciones severas a nivel de kernel de sistema operativo. Estos contenedores tendrán prohibido el acceso a la red interna de la organización y su ciclo de vida útil se limitará a la ejecución de la tarea específica, destruyéndose y recreándose desde una imagen limpia e inmutable inmediatamente después de finalizar la inferencia.

        

### 4.2. Inspección del Chain-of-Thought (Cadena de Razonamiento)

        Para evitar ataques avanzados donde el agente intente engañar a las capas de control mediante razonamientos encubiertos u ocultamiento de intenciones, el microservicio de orquestación (Middleware) interceptará obligatoriamente los tokens de razonamiento generados internamente por el modelo antes de enviar la respuesta final al usuario o al actuador de la API. Si en dicha cadena de pensamiento se detectan secuencias de comandos de escape, intenciones de exfiltración de datos corporativos o manipulación de sus propias directrices del sistema, la ejecución se congelará ipso facto.

        

## 5. IMPLEMENTACIÓN DE REFERENCIA (COMPLIANCE ENGINE EN RUST)

        Para garantizar el máximo rendimiento técnico, la inmutabilidad de la lógica de control y la exclusión de vulnerabilidades comunes de desbordamiento de memoria, las compuertas de validación de conformidad y puntuación de riesgo en los microservicios core de la organización se implementan bajo el lenguaje de programación Rust.

        
        El siguiente bloque representa el código base del componente operativo encargado de evaluar las respuestas de los usuarios, calcular los niveles de riesgo normativo según las variables del negocio y gatillar acciones automatizadas conforme a las directrices de este manual.

        use axum::{routing::{get, post}, Json, Router};
use serde::{Deserialize, Serialize};

#[derive(Serialize)]
struct Question {
    id: u32,
    text: String,
    weight: u32,
}

#[derive(Deserialize)]
struct Answer {
    id: u32,
    yes: bool,
}

#[derive(Serialize)]
struct ResultScore {
    score: u32,
    level: String,
    requires_kill_switch: bool,
}

async fn health() -> &'static str {
    "CheckWizard IA Compliance Engine MVP OK"
}

async fn questions() -> Json<Vec<Question>> {
    Json(vec![
        Question { id: 1, text: String::from("¿Existe inventario de datos personales y trazabilidad de procedencia?"), weight: 25 },
        Question { id: 2, text: String::from("¿El sistema cuenta con un panel de supervisión humana efectiva (Human-in-the-loop)?"), weight: 25 },
        Question { id: 3, text: String::from("¿Los pesos del modelo cuentan con verificación de hash SHA-256 en pre-carga?"), weight: 25 },
        Question { id: 4, text: String::from("¿El agente opera en un entorno sandbox aislado sin acceso directo a bases de datos core?"), weight: 25 },
    ])
}

async fn evaluate(Json(answers): Json<Vec<Answer>>) -> Json<ResultScore> {
    // Evaluación probabilística de la madurez del control de ciberseguridad algorítmica
    let score: u32 = answers.iter().filter(|a| a.yes).count() as u32 * 25;

    let level = match score {
        90..=100 => "Excelente - Conforme ISO 42001 y Ley 21.719",
        75..=89 => "Alto - Cumplimiento Base Satisfactorio",
        50..=74 => "Medio - Requiere Acciones Correctivas Inmediatas",
        25..=49 => "Alto Riesgo - Vulnerable a Subversión Algorítmica",
        _ => "Crítico - Incumplimiento Normativo y Técnico Gravísimo",
    };

    // Gatillo automatizado: Si el score es crítico o de alto riesgo, se activa la bandera de Kill Switch
    let kill_switch = score < 50;

    Json(ResultScore {
        score,
        level: level.to_string(),
        requires_kill_switch: kill_switch,
    })
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/health", get(health))
        .route("/questions", get(questions))
        .route("/evaluate", post(evaluate));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

        

## 6. INTEGRACIÓN TAXONÓMICA DE INCIDENTES (ANCI CHILE)

        Ante la materialización de un evento que afecte a los modelos (fuga de datos de entrenamiento por inversión de pertenencia, alteración de la lógica interna por inyección de prompts, o denegación de servicio algorítmico), el CISO clasificará el incidente utilizando los efectos observables dictados por la Resolución Exenta N° 7 de 2025 de la Agencia Nacional de Ciberseguridad (ANCI), garantizando la consistencia legal de los reportes obligatorios:

        
            
- Área B - Confidencialidad de la Información (Efecto B.1 Exfiltración): Activado si el modelo sufre un ataque de extracción o reconstrucción que exponga datos personales chilenos en el output de usuarios públicos.

            
- Área D - Integridad de la Información (Efecto D.1 Alteración del Sistema): Activado de forma inmediata si se detecta la alteración persistente de los pesos neuronales o el desvío intencional de la lógica de inferencia a través de un exploit o backdoor. Genera el reporte obligatorio e ineludible al CSIRT Nacional en los plazos fijados por la Ley N° 21.663.