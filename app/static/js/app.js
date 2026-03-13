let allPokemon = [];
let filteredPokemon = [];
let selectedTypes = [];
let searchQuery = "";

const statNames = {
    'hp': 'HP',
    'attack': '攻击',
    'defense': '防御',
    'special-attack': '特攻',
    'special-defense': '特防',
    'speed': '速度'
};

const evolutionTriggerNames = {
    'level-up': '升级',
    'trade': '交换',
    'use-item': '使用道具',
    'other': '其他'
};

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

async function loadPokemon() {
    const loading = document.getElementById('loading');
    const grid = document.getElementById('pokemon-grid');
    
    try {
        const response = await fetch('/api/pokemon');
        const data = await response.json();
        allPokemon = data.pokemon;
        filteredPokemon = [...allPokemon];
        renderPokemon();
    } catch (error) {
        console.error('Failed to load pokemon:', error);
        loading.innerHTML = '<p>加载失败，请刷新页面重试</p>';
        return;
    }
    
    loading.style.display = 'none';
    grid.style.display = 'grid';
}

function renderPokemon() {
    const grid = document.getElementById('pokemon-grid');
    const noResults = document.getElementById('no-results');
    
    if (filteredPokemon.length === 0) {
        grid.style.display = 'none';
        noResults.style.display = 'block';
        return;
    }
    
    grid.style.display = 'grid';
    noResults.style.display = 'none';
    
    grid.innerHTML = filteredPokemon.map(pokemon => {
        const typeTags = pokemon.types.map(type => 
            `<span class="type-tag" style="background-color: ${typeColors[type]}">${typeNamesZh[type] || type}</span>`
        ).join('');
        
        return `
            <a href="/pokemon/${pokemon.id}" class="pokemon-card" 
               style="--card-type-color-1: ${pokemon.type_colors[0]}; --card-type-color-2: ${pokemon.type_colors[1] || pokemon.type_colors[0]}">
                <div class="pokemon-id">#${String(pokemon.id).padStart(3, '0')}</div>
                <img class="pokemon-image" src="${pokemon.image_url}" alt="${pokemon.name}" loading="lazy">
                <div class="pokemon-name">${pokemon.name}</div>
                ${pokemon.name_zh ? `<div class="pokemon-name-zh">${pokemon.name_zh}</div>` : ''}
                <div class="pokemon-types">${typeTags}</div>
            </a>
        `;
    }).join('');
}

function filterPokemon() {
    filteredPokemon = allPokemon.filter(pokemon => {
        const matchesSearch = searchQuery === '' || 
            pokemon.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            (pokemon.name_zh && pokemon.name_zh.includes(searchQuery)) ||
            String(pokemon.id) === searchQuery ||
            String(pokemon.id).padStart(3, '0').includes(searchQuery);
        
        const matchesTypes = selectedTypes.length === 0 ||
            selectedTypes.every(type => pokemon.types.includes(type));
        
        return matchesSearch && matchesTypes;
    });
    
    renderPokemon();
}

function handleSearch(event) {
    searchQuery = event.target.value.trim();
    
    const clearBtn = document.getElementById('clear-search');
    if (searchQuery) {
        clearBtn.classList.add('visible');
    } else {
        clearBtn.classList.remove('visible');
    }
    
    filterPokemon();
}

function clearSearch() {
    const searchInput = document.getElementById('search-input');
    searchInput.value = '';
    searchQuery = '';
    document.getElementById('clear-search').classList.remove('visible');
    filterPokemon();
}

function handleTypeFilter(event) {
    const btn = event.target.closest('.type-filter-btn');
    if (!btn) return;
    
    const type = btn.dataset.type;
    const index = selectedTypes.indexOf(type);
    
    if (index === -1) {
        selectedTypes.push(type);
        btn.classList.add('active');
    } else {
        selectedTypes.splice(index, 1);
        btn.classList.remove('active');
    }
    
    filterPokemon();
}

function clearFilters() {
    selectedTypes = [];
    document.querySelectorAll('.type-filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    filterPokemon();
}

async function loadPokemonDetail() {
    const loading = document.getElementById('loading');
    const content = document.getElementById('detail-content');
    
    try {
        const response = await fetch(`/api/pokemon/${pokemonId}`);
        const data = await response.json();
        
        const pokemon = data.pokemon;
        const evolution = data.evolution;
        
        document.getElementById('pokemon-image').src = pokemon.image_url;
        document.getElementById('pokemon-image').alt = pokemon.name;
        document.getElementById('pokemon-id').textContent = `#${String(pokemon.id).padStart(3, '0')}`;
        document.getElementById('pokemon-name').textContent = pokemon.name;
        document.getElementById('pokemon-name-zh').textContent = pokemon.name_zh || '';
        document.getElementById('pokemon-genus').textContent = pokemon.genus || '';
        document.getElementById('pokemon-height').textContent = `${pokemon.height} m`;
        document.getElementById('pokemon-weight').textContent = `${pokemon.weight} kg`;
        document.getElementById('pokemon-description').textContent = pokemon.description || '暂无描述';
        
        const typesContainer = document.getElementById('pokemon-types');
        typesContainer.innerHTML = pokemon.types.map(type => 
            `<span class="type-tag" style="background-color: ${typeColors[type]}">${typeNamesZh[type] || type}</span>`
        ).join('');
        
        const statsContainer = document.getElementById('stats-container');
        statsContainer.innerHTML = Object.entries(pokemon.stats).map(([stat, value]) => {
            const percentage = Math.min((value / 255) * 100, 100);
            const color = value >= 100 ? '#4caf50' : value >= 60 ? '#ff9800' : '#f44336';
            return `
                <div class="stat-item">
                    <span class="stat-name">${statNames[stat] || stat}</span>
                    <div class="stat-bar-container">
                        <div class="stat-bar" style="width: ${percentage}%; background-color: ${color}"></div>
                    </div>
                    <span class="stat-value">${value}</span>
                </div>
            `;
        }).join('');
        
        if (evolution && evolution.length > 0) {
            const evolutionSection = document.getElementById('evolution-section');
            const evolutionChain = document.getElementById('evolution-chain');
            evolutionSection.style.display = 'block';
            
            let evolutionHTML = '';
            for (let i = 0; i < evolution.length; i++) {
                const stage = evolution[i];
                
                for (let j = 0; j < stage.length; j++) {
                    const evo = stage[j];
                    const isCurrent = evo.id === pokemonId;
                    evolutionHTML += `
                        <a href="/pokemon/${evo.id}" class="evolution-item ${isCurrent ? 'current' : ''}">
                            <img class="evolution-image" src="${evo.image_url}" alt="${evo.name}" loading="lazy">
                            <div class="evolution-name">${evo.name}</div>
                            ${evo.name_zh ? `<div class="evolution-name-zh">${evo.name_zh}</div>` : ''}
                        </a>
                    `;
                    
                    if (j < stage.length - 1) {
                        evolutionHTML += '<span class="evolution-arrow">/</span>';
                    }
                }
                
                if (i < evolution.length - 1 && evolution[i + 1].length > 0) {
                    const nextStage = evolution[i + 1][0];
                    let triggerText = '';
                    if (nextStage.trigger) {
                        triggerText = evolutionTriggerNames[nextStage.trigger] || nextStage.trigger;
                    }
                    if (nextStage.level) {
                        triggerText += ` Lv.${nextStage.level}`;
                    }
                    if (nextStage.item) {
                        triggerText += ` ${nextStage.item}`;
                    }
                    
                    evolutionHTML += `
                        <div class="evolution-trigger">
                            <span class="evolution-arrow">→</span>
                            ${triggerText ? `<span>${triggerText}</span>` : ''}
                        </div>
                    `;
                }
            }
            
            evolutionChain.innerHTML = evolutionHTML;
        }
        
    } catch (error) {
        console.error('Failed to load pokemon detail:', error);
        loading.innerHTML = '<p>加载失败，请返回重试</p>';
        return;
    }
    
    loading.style.display = 'none';
    content.style.display = 'block';
}

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const clearSearchBtn = document.getElementById('clear-search');
    const typeFilters = document.getElementById('type-filters');
    const clearFiltersBtn = document.getElementById('clear-filters');
    
    if (searchInput) {
        searchInput.addEventListener('input', debounce(handleSearch, 300));
        loadPokemon();
    }
    
    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', clearSearch);
    }
    
    if (typeFilters) {
        typeFilters.addEventListener('click', handleTypeFilter);
    }
    
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', clearFilters);
    }
    
    if (typeof pokemonId !== 'undefined') {
        loadPokemonDetail();
    }
});
