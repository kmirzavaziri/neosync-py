if (value === null) {
  return null;
}

if (!value) {
  return '';
}

return neosync.generateRandomString({
  min: 30,
  max: 50
});
