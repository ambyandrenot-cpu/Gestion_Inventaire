// Variables globales
let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();
let deviceData = {};
let archives = [];
let editingId = null;

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    updateMonthTabs();
    initializeData();
    
    // Événements
    document.getElementById('deviceForm').addEventListener('submit', saveDevice);
    document.getElementById('emailForm').addEventListener('submit', sendEmail);
    document.getElementById('searchInput').addEventListener('keyup', filterTable);
    document.getElementById('workplace').addEventListener('change', filterTable);
    
    // Fermeture des menus déroulants en cliquant ailleurs
    document.addEventListener('click', function(event) {
        const exportMenu = document.getElementById('exportMenu');
        const exportButton = event.target.closest('button[onclick="toggleExportMenu()"]');
        
        if (!exportButton && exportMenu.classList.contains('block')) {
            exportMenu.classList.remove('block');
            exportMenu.classList.add('hidden');
        }
    });
});

// Mise à jour des onglets des mois
function updateMonthTabs() {
    const months = [
        'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 
        'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
    ];
    
    let currentDate = new Date();
    currentDate.setMonth(currentMonth);
    currentDate.setFullYear(currentYear);
    
    let prevDate1 = new Date(currentDate);
    prevDate1.setMonth(currentDate.getMonth() - 1);
    
    let prevDate2 = new Date(currentDate);
    prevDate2.setMonth(currentDate.getMonth() - 2);
    
    document.getElementById('month-name-current').textContent = `${months[currentDate.getMonth()]} ${currentDate.getFullYear()}`;
    document.getElementById('month-name-1').textContent = `${months[prevDate1.getMonth()]} ${prevDate1.getFullYear()}`;
    document.getElementById('month-name-2').textContent = `${months[prevDate2.getMonth()]} ${prevDate2.getFullYear()}`;
}

// Changement de mois actif
function changeMonth(offset) {
    const tabs = [
        document.getElementById('tab-month-2'),
        document.getElementById('tab-month-1'),
        document.getElementById('tab-current')
    ];
    
    tabs.forEach(tab => {
        tab.classList.remove('tab-active');
        tab.classList.add('btn-secondary');
    });
    
    if (offset === -2) {
        tabs[0].classList.remove('btn-secondary');
        tabs[0].classList.add('tab-active');
    } else if (offset === -1) {
        tabs[1].classList.remove('btn-secondary');
        tabs[1].classList.add('tab-active');
    } else {
        tabs[2].classList.remove('btn-secondary');
        tabs[2].classList.add('tab-active');
    }
    
    loadMonthData(offset);
}

// Chargement des données du mois
function loadMonthData(offset) {
    const now = new Date();
    const targetMonth = new Date(now.getFullYear(), now.getMonth() + offset, 1);
    currentMonth = targetMonth.getMonth();
    currentYear = targetMonth.getFullYear();
    
    updateMonthTabs();
    
    const monthKey = `${currentYear}-${currentMonth + 1}`;
    
    if (!deviceData[monthKey]) {
        deviceData[monthKey] = [];
    }
    
    renderTable();
}

// Initialisation des données
function initializeData() {
    const savedData = localStorage.getItem('gardnetDeviceData');
    const savedArchives = localStorage.getItem('gardnetArchives');
    
    if (savedData) {
        deviceData = JSON.parse(savedData);
    } else {
        deviceData = {};
    }
    
    if (savedArchives) {
        archives = JSON.parse(savedArchives);
    }
    
    loadMonthData(0);
}

// Sauvegarde des données
function saveData() {
    localStorage.setItem('gardnetDeviceData', JSON.stringify(deviceData));
}

// Sauvegarde des archives
function saveArchives() {
    localStorage.setItem('gardnetArchives', JSON.stringify(archives));
}

// Affichage du tableau des appareils
function renderTable() {
    const tableBody = document.getElementById('deviceTableBody');
    tableBody.innerHTML = '';
    
    const monthKey = `${currentYear}-${currentMonth + 1}`;
    const selectedWorkplace = document.getElementById('workplace').value;
    const searchText = document.getElementById('searchInput').value.toLowerCase();
    
    let filteredData = deviceData[monthKey] || [];
    
    if (selectedWorkplace !== 'all') {
        filteredData = filteredData.filter(device => 
            device.workplace && device.workplace.toLowerCase().includes(selectedWorkplace.toLowerCase())
        );
    }
    
    if (searchText) {
        filteredData = filteredData.filter(device => 
            (device.clientName && device.clientName.toLowerCase().includes(searchText)) ||
            (device.serialNumber && device.serialNumber.toLowerCase().includes(searchText)) ||
            (device.deviceType && device.deviceType.toLowerCase().includes(searchText)) ||
            (device.workplace && device.workplace.toLowerCase().includes(searchText))
        );
    }
    
    filteredData.forEach((device, index) => {
        const row = document.createElement('tr');
        
        // Classes de couleur selon l'état
        let statusClass = '';
        if (device.status === 'Mauvais') {
            statusClass = 'text-yellow-600 font-medium';
        } else if (device.status === 'Défectueux') {
            statusClass = 'text-red-600 font-medium';
        } else {
            statusClass = 'text-green-600 font-medium';
        }
        
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${device.clientName}</td>
            <td>${device.workplace || ''}</td>
            <td>${device.deviceType}</td>
            <td>${device.serialNumber}</td>
            <td class="${statusClass}">${device.status}</td>
            <td class="no-print">
                <div class="flex space-x-2">
                    <button class="text-blue-600 hover:text-blue-800" onclick="editDevice(${device.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="text-red-600 hover:text-red-800" onclick="deleteDevice(${device.id})">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            </td>
        `;
        
        tableBody.appendChild(row);
    });
}

// Filtrage du tableau
function filterTable() {
    renderTable();
}

// Affichage du formulaire d'ajout
function showAddForm() {
    document.getElementById('modalTitle').textContent = 'Ajouter un appareil';
    document.getElementById('deviceForm').reset();
    document.getElementById('editId').value = '';
    document.getElementById('newDeviceTypeForm').classList.add('hidden');
    
    const modal = document.getElementById('deviceModal');
    modal.classList.remove('hidden');
}

// Affichage du formulaire de type d'appareil
function showNewDeviceTypeForm() {
    const form = document.getElementById('newDeviceTypeForm');
    form.classList.toggle('hidden');
}

// Ajout d'un nouveau type d'appareil
function addNewDeviceType() {
    const newType = document.getElementById('newDeviceType').value.trim();
    
    if (newType) {
        const deviceTypeSelect = document.getElementById('deviceType');
        const option = document.createElement('option');
        option.value = newType;
        option.textContent = newType;
        deviceTypeSelect.appendChild(option);
        option.selected = true;
        
        document.getElementById('newDeviceTypeForm').classList.add('hidden');
        document.getElementById('newDeviceType').value = '';
    }
}

// Sauvegarde d'un appareil
function saveDevice(e) {
    e.preventDefault();
    
    const clientName = document.getElementById('clientName').value;
    const workplace = document.getElementById('workplaceInput').value;
    const deviceType = document.getElementById('deviceType').value;
    const serialNumber = document.getElementById('serialNumber').value;
    const status = document.getElementById('deviceStatus').value;
    const editId = document.getElementById('editId').value;
    
    const monthKey = `${currentYear}-${currentMonth + 1}`;
    
    if (!deviceData[monthKey]) {
        deviceData[monthKey] = [];
    }
    
    // Vérification du numéro de série en double
    const isDuplicate = deviceData[monthKey].some(device => 
        device.serialNumber === serialNumber && 
        (editId === '' || parseInt(editId) !== device.id)
    );
    
    if (isDuplicate) {
        Swal.fire({
            title: 'Attention !',
            text: 'Ce numéro de série existe déjà dans la base de données.',
            icon: 'warning',
            confirmButtonText: 'OK',
            confirmButtonColor: '#1e40af'
        });
        return;
    }
    
    if (editId) {
        // Mode édition
        const index = deviceData[monthKey].findIndex(device => device.id === parseInt(editId));
        
        if (index !== -1) {
            deviceData[monthKey][index] = {
                id: parseInt(editId),
                clientName,
                workplace,
                deviceType,
                serialNumber,
                status
            };
        }
    } else {
        // Mode ajout
        const newId = generateId();
        
        deviceData[monthKey].push({
            id: newId,
            clientName,
            workplace,
            deviceType,
            serialNumber,
            status
        });
    }
    
    saveData();
    renderTable();
    closeModal();
    
    Swal.fire({
        title: 'Succès !',
        text: editId ? 'Appareil modifié avec succès.' : 'Appareil ajouté avec succès.',
        icon: 'success',
        confirmButtonText: 'OK',
        confirmButtonColor: '#1e40af'
    });
}

// Génération d'un ID unique
function generateId() {
    return Date.now();
}

// Édition d'un appareil
function editDevice(id) {
    const monthKey = `${currentYear}-${currentMonth + 1}`;
    const device = deviceData[monthKey].find(d => d.id === id);
    
    if (device) {
        document.getElementById('modalTitle').textContent = 'Modifier un appareil';
        document.getElementById('clientName').value = device.clientName || '';
        document.getElementById('workplaceInput').value = device.workplace || '';
        
        const deviceTypeSelect = document.getElementById('deviceType');
        let option = Array.from(deviceTypeSelect.options).find(opt => opt.value === device.deviceType);
        
        if (!option) {
            option = document.createElement('option');
            option.value = device.deviceType;
            option.textContent = device.deviceType;
            deviceTypeSelect.appendChild(option);
        }
        
        deviceTypeSelect.value = device.deviceType;
        document.getElementById('serialNumber').value = device.serialNumber || '';
        document.getElementById('deviceStatus').value = device.status;
        document.getElementById('editId').value = device.id;
        
        document.getElementById('deviceModal').classList.remove('hidden');
    }
}

// Suppression d'un appareil
function deleteDevice(id) {
    Swal.fire({
        title: 'Êtes-vous sûr ?',
        text: 'Cette action est irréversible!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Oui, supprimer',
        cancelButtonText: 'Annuler',
        confirmButtonColor: '#dc2626',
        cancelButtonColor: '#4b5563'
    }).then((result) => {
        if (result.isConfirmed) {
            const monthKey = `${currentYear}-${currentMonth + 1}`;
            deviceData[monthKey] = deviceData[monthKey].filter(device => device.id !== id);
            
            saveData();
            renderTable();
            
            Swal.fire({
                title: 'Supprimé !',
                text: 'L\'appareil a été supprimé avec succès.',
                icon: 'success',
                confirmButtonText: 'OK',
                confirmButtonColor: '#1e40af'
            });
        }
    });
}

// Fermeture du modal
function closeModal() {
    document.getElementById('deviceModal').classList.add('hidden');
}

// Gestion du menu d'exportation
function toggleExportMenu() {
    const menu = document.getElementById('exportMenu');
    menu.classList.toggle('hidden');
    menu.classList.toggle('block');
}

// Exportation en Excel
function exportToExcel() {}