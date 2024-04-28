# Проверяем наличие виртуального окружения
if (Test-Path ./venv/Scripts/Activate.ps1) {
    Write-Host "Virtual environment exists. Activating..."
    # Активируем виртуальное окружение
    ./venv/Scripts/Activate.ps1
} else {
    Write-Host "Virtual environment does not exist. Creating..."
    # Создаем виртуальное окружение
    python -m venv venv
    Write-Host "Virtual environment created. Activating..."
    # Активируем виртуальное окружение
    ./venv/Scripts/Activate.ps1
}