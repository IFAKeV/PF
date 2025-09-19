const events = [
  {
    title: 'Big Knock',
    date: 't.b.a.',
    location: 'Care Ashore<br>Springbok Est<br>Dunsfold Rd<br>Alfold GU6 8EX',
    locationlink: 'https://maps.app.goo.gl/z1oV15RKgvrFVK117',
    description: 'You can arrive a few days early. We are on the far side of the main house - clockwise round the walled Garden road & turn in by the tall fir trees.',
    link: 'http://www.dieselbike.net/'
  },
  {
    title: 'Bergrennen Gaschney',
    date: 't.b.a.',
    location: 'Muhlbach sur Munster',
    locationlink: 'https://maps.app.goo.gl/o2uTmQCTyjmi6NiU9',
    description: 'Course ZUE et Championnats de Suisse FHRM et SMLT.',
    link: 'https://www.nouveau-moto-club-de-munster.net/'
  },
  {
    title: 'Sommer Dieseltreffen',
    date: '16. August 2026',
    location: 'Geyern',
    locationlink: 'https://maps.app.goo.gl/rFyRxo9JQ396umCk9',
    description: 'Teams treten am Strand gegeneinander an.',
    link: 'http://sommerdiesel.de/'
  },
  {
    title: 'Internationales Dieselmotorradtreffen 2026',
    date: 't.b.a.',
    location: 'Zeltplatz Abenteuerland, 34414 Warburg/Bonenburg',
    locationlink: 'https://maps.app.goo.gl/EnnN6AnAPVpbUMdH7',
    description: 'Wanderung durch die ersten Herbstfarben.'
  }
];

const container = document.getElementById('cards-container');

function createCard(event) {
  const card = document.createElement('div');
  card.className = 'card';

  card.innerHTML = `
    <h2>${event.title}</h2>
    <p><strong>Datum:</strong> ${event.date}</p>
    <p><strong>Ort:</strong> ${event.location}</p>
    <p>${event.description}</p>
    <p>${event.link}</p>
  `;

  return card;
}

events.forEach(event => {
  const card = createCard(event);
  container.appendChild(card);
});
